from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from starlette import status

router = APIRouter()


class Doctor:
    id: int
    name: str
    specialization: str
    phone: int
    is_available: bool = True

    def __init__(self, id, name, specialty, phone, is_available):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.phone = phone
        self.is_available = is_available

class NewDoctor(BaseModel):
    id: int
    name: str
    specialty: str
    phone: int
    is_available: bool


    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'name': 'Dr. Smith',
                'specialty': 'Cardiology',
                'phone': 1234567890,
                'is_available': True
            }
        }


DOCTOR = [
    Doctor(1, 'Ahmed Duke', 'Surgeon', 700000001, is_available=True),
    Doctor(2, 'Joe Simmons', 'Pediatrician', 700000002, is_available=True),
    Doctor(3, 'Liam Wong', 'Cardiologist', 700000003, is_available=False),
    Doctor(4, 'Olivia Chen', 'Neurologist', 700000004, is_available=True),
    Doctor(5, 'Sophia Patel', 'Orthopedic', 7000000005, is_available=False)
]


#CRUD FOR DOCTORS


@router.get("/doctor/", status_code=status.HTTP_200_OK)
async def read_all_doctors():
    return DOCTOR



@router.get("/doctor/{doctor_id}", response_model=NewDoctor, status_code=status.HTTP_200_OK)
async def read_doctor(doctor_id: int):
    for doctor in DOCTOR:
        if doctor_id == doctor.id:
            return doctor
    raise HTTPException(status_code=404, detail='Doctor Not found')


@router.post("/create_doctor", response_model=NewDoctor, status_code=status.HTTP_201_CREATED)
async def create_doctor(new_doctor: NewDoctor):
    doctor = Doctor(
       id=new_doctor.id,
       name=new_doctor.name,
       phone=new_doctor.phone,
       specialty=new_doctor.specialty,
       is_available=new_doctor.is_available
    )
    DOCTOR.append(doctor)
    return doctor


@router.put("/doctor/update_doctor", status_code=status.HTTP_204_NO_CONTENT)
async def update_doctor(doctor: NewDoctor):
    doctor_changed = False
    for i in range(len(DOCTOR)):
        if DOCTOR[i].id == doctor.id:
            DOCTOR[i] = doctor
            doctor_changed = True
    if not doctor_changed:
        raise HTTPException(status_code=404, detail='Doctor not found')


@router.delete("/doctor/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: int):
    doctor_changed = False
    for i in range (len(DOCTOR)):
        if DOCTOR[i].id == doctor_id:
            DOCTOR.pop(i)
            doctor_changed = True
            break
    if not doctor_changed:
        raise HTTPException(status_code=404, detail='patient not found')

