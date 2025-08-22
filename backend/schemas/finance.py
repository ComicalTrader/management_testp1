from pydantic import BaseModel
from datetime import datetime

class FinanceCreate(BaseModel):
    description: str
    amount: float
    type: str  # "income" ou "expense"
    date: datetime | None = None  # opcional, se não informado usa datetime.utcnow()

class FinanceOut(FinanceCreate):
    id: int

    class Config:
        from_attributes = True  # permite converter SQLAlchemy → Pydantic
