from fastapi import FastAPI
from schemas import AppointmentCreate
from barber_app.schemas import AppointmentCreate



app = FastAPI()

@app.post("/appointments")
def create_appointment(data: AppointmentCreate):
    return {"message": f"{data.customer_name} uchun navbat saqlandi!"}
