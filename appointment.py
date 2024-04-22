from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from starlette import status

from routers.doctor import DOCTOR

router = APIRouter()


class APPOINTMENT:
    id: int
    patient_id: int
    doctor_id: int
    date: str

    def __init__(self, id, patient_id, doctor_id, date):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date


class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'patient_id': 2,
                'doctor_id': 2,
                'date': '2020-04-01'

            }
        }


APPOINTMENT_DATA = [
    Appointment(id=1, patient_id=1, doctor_id=2, date='2024-05-02', ),
    Appointment(id=2,  patient_id=1, doctor_id=1, date='2024-04-03', ),
    Appointment(id=3, patient_id=1, doctor_id=3, date='2024-03-02', ),
    Appointment(id=3, patient_id=1, doctor_id=3, date='2024-02-09', ),
    Appointment(id=3, patient_id=1, doctor_id=3, date='2024-01-08', )
]


# CRUD FOR APPOINTMENT
@router.get("/appointments", response_model=Appointment)
async def get_appointments():
    return APPOINTMENT_DATA


@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: int):
    for appointment in APPOINTMENT_DATA:
        if appointment.id == appointment_id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")


@router.put("/appointment/{appointment_id}")
async def update_appointment(appointment_id: int, update_data: Appointment):
    if appointment_id < 0 or appointment_id >= len(APPOINTMENT_DATA):
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment = APPOINTMENT_DATA[appointment_id]
    if update_data.patient_id is not None:
        appointment.patient_id = update_data.patient_id
    if update_data.doctor_id is not None:
        appointment.doctor_id = update_data.doctor_id
    if update_data.date is not None:
        appointment.date = update_data.date

    return {"message": "Appointment updated successfully", "appointment": appointment}


@router.post("/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: Appointment):
    # Check if the doctor is available
    doctor_available = False
    for doctor in DOCTOR:
        if doctor.id == appointment.doctor_id and doctor.is_available:
            doctor_available = True
            break
    if not doctor_available:
        raise HTTPException(status_code=400, detail="Doctor not available")

    # Check if the patient has existing appointments
    for existing_appointment in APPOINTMENT_DATA:
        if existing_appointment.patient_id == appointment.patient_id:
            raise HTTPException(status_code=400, detail="Patient already has an existing appointment")

    APPOINTMENT_DATA.append(appointment)
    return appointment


@router.delete("/appointments/{appointment_id}", status_code=204)
async def delete_appointment(appointment_id: int):
    for i, appointment in enumerate(APPOINTMENT_DATA):
        if appointment.id == appointment_id:
            del APPOINTMENT_DATA[i]
            return
    raise HTTPException(status_code=404, detail="Appointment not found")