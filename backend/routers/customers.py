from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.customers import Customer
from ..schemas.customers import CustomerCreate, CustomerOut





router = APIRouter(prefix="/customers", tags=["customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    obj = Customer(**customer.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# LIST ALL
@router.get("/", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

# GET BY ID
@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Customer).filter(Customer.id == customer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    return obj

# UPDATE
@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    obj = db.query(Customer).filter(Customer.id == customer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer.model_dump().items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

# DELETE
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Customer).filter(Customer.id == customer_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}
