from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    contact: str | None = None
    notes: str | None = None

class CustomerOut(CustomerCreate):
    id: int

    class Config:
        from_attributes = True
