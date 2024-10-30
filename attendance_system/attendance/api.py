# attendance/api.py
from ninja import NinjaAPI
from pydantic import BaseModel
from .models import Attendance
from django.utils import timezone

# Initialize the Ninja API
api = NinjaAPI()

# Schema for the incoming data
class AttendanceSchema(BaseModel):
    person_id: int

# View to handle attendance registration
@api.get("/register")
def register_attendance(request, payload: AttendanceSchema):
    # Create a new attendance entry in the database with the current timestamp
    attendance = Attendance.objects.create(
        person_id=payload.person_id,
        arrival_time=timezone.now()
    )
    return {"id": attendance.id, "person_name": attendance.first_name, "arrival_time": attendance.arrival_time}
@api.post("/registerpost")
def register_attendance(request, payload: AttendanceSchema):
    # Create a new attendance entry in the database with the current timestamp
    attendance = Attendance.objects.create(
        person_id=payload.person_id,
        arrival_time=timezone.now()
    )
    return {"id": attendance.id, "person_name": attendance.first_name, "arrival_time": attendance.arrival_time}