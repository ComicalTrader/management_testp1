from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    customer_name: str; phone: str | None = None
    service: str; start_at: datetime; notes: str | None = None


class AppointmentOut(AppointmentCreate):
    id:int
    
    class Config: from_attributes = True
    