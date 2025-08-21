from sqlalchemy import Column,Integer,String,DateTime
from ..database import base

class Appointment(base):
    __tablename__ = "appointment"
    id = Column(Integer,primary_key = True,index = True)
    custommer_name = Column(String, index = True)
    phone = Column(String)
    start_at = Column(DateTime, index = True)
    notes = Column(String)
    