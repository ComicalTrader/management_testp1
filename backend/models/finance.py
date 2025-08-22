from sqlalchemy import Column,Integer,String,DateTime,Float
import datetime
from ..database import Base


class Finance(Base):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    type = Column(String)  # "income" ou "expense"
    date = Column(DateTime, default=datetime.datetime.utcnow)