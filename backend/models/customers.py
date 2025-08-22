from sqlalchemy import Column,Integer,String,DateTime,Float
import datetime
from ..database import Base

class Customer(Base):

    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact = Column(String)
    notes = Column(String, default="")
    