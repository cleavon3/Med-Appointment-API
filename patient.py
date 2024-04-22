from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from starlette import status

router = APIRouter()

class Patient:
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: int

    def __init__(self, id, name, age, sex, weight, height, phone):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.phone = phone


class NewPatient(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    sex: str
    weight: float = Field(gt=-1, lt=100)
    height: float = Field(gt=-1, lt=100)
    phone: int

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'A new patient',
                'age': 25,
                'sex': 'M',
                'weight': 71.0,
                'height': 1.72,
                'phone': 800000001
            }
        }

PATIENT = [
    Patient(1, 'john gift', '25', 'M', '71', '1.72', 800000001),
    Patient(2, 'Maximo Chen', '40', 'M', '82', '1.80', 800000002),
    Patient(3, 'Jasper Cruz', '48', 'F', '90', '1.90', 800000003),
    Patient(4, 'Aurora Knight', '33', 'M', '67', '1.00', 800000004),
    Patient(5, 'Nova Singh', '34', 'M', '75', '1.90', 8000000005),
    Patient(6, 'Phoenix Li', '30', 'F', '65', '2.00', 800000006)
]


#CRUD FOR PATIENT

@router.get("/patient", status_code=status.HTTP_200_OK)
async def read_all_patient():
    return PATIENT


@router.get("/patient/{patient_id}" , status_code=status.HTTP_200_OK)
async def read_patient(patient_id: int):
    for patient in PATIENT:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail='Patient Not found')

@router.get("/patient/", status_code=status.HTTP_200_OK)
async def read_patient_by_phone(patient_phone: int):
    phone_to_return = []
    for patient in PATIENT:
        if patient.phone == patient_phone:
            phone_to_return.append(patient)
    return phone_to_return


@router.post("/create-patient", status_code=status.HTTP_201_CREATED)
async def create_patient(new_patient: NewPatient):
    new_patient = Patient(**new_patient.dict())
    PATIENT.append(find_patient_id(new_patient))


def find_patient_id(patient: Patient):
    patient.id = 1 if len(PATIENT) == 0 else PATIENT[-1].id + 1
    return patient

@router.put("/patient/update_patient", status_code=status.HTTP_204_NO_CONTENT)
async def update_patient(patient: NewPatient):
    patient_changed = False
    for i in range(len(PATIENT)):
        if PATIENT[i].id == patient.id:
            PATIENT[i] = patient
            patient_changed = True
    if not patient_changed:
        raise HTTPException(status_code=404, detail='patient not found')



@router.delete("/patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int):
    patient_changed = False
    for i in range (len(PATIENT)):
        if PATIENT[i].id == patient_id:
            PATIENT.pop(i)
            patient_changed = True
            break
    if not patient_changed:
        raise HTTPException(status_code=404, detail='patient not found')

