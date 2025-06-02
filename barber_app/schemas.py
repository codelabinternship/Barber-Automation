from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Appointment(BaseModel):
    clientName: str
    dateTime: datetime
    service: str

    class Config:
        schema_extra = {
            "example": {
                "clientName": "Ali",
                "dateTime": "2025-06-10T14:00:00Z",
                "service": "Haircut"
            }
        }

@app.post("/appointments")
async def create_appointment(appointment: Appointment):
    return {"message": "Appointment created", "appointment": appointment}
