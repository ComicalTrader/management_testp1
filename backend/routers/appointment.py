from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.appointment import Appointment
from ..schemas.appointment import AppointmentCreate,AppointmentOut


router = APIRouter(prefix = "/appointment", tags = ["appointment"])


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()



@router.post("/",response_model=AppointmentOut,tags=["Appointments"], summary="Criar novo agendamento", description="Cria um novo agendamento no sistema de barbearia.")
def create(ap:AppointmentCreate, db: Session = Depends(get_db)):
    obj = Appointment(**ap.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj



@router.get("/",response_model= list [AppointmentOut])
def list_all(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return appointments



@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"message": "Deleted successfully"}


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, ap: AppointmentCreate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    for key, value in ap.model_dump().items():
        setattr(appt, key, value)
    
    db.commit()
    db.refresh(appt)
    return appt