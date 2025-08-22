from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.appointment import Appointment
from ..schemas.appointment import AppointmentCreate,AppointmentOut


router = APIRouter(prefix = "/appointments", tags = ["appointments"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()



@router.post("",response_model=AppointmentOut)
def create(ap:AppointmentCreate, db: Session = Depends(get_db)):
    obj = Appointment(**ap.model_dump)
    db.add(obj); db.commit(); db.refresh(obj); return obj



@router.get("",response_model= list [AppointmentOut])
def list_all(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

