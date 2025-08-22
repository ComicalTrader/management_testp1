from sqlalchemy import Column,Integer,String,DateTime,Float
import datetime
from ..database import Base

class Appointment(Base):

    __tablename__ = "appointment"

    id = Column(Integer,primary_key = True,index = True)
    customer_name = Column(String, index = True)
    phone = Column(String)
    start_at = Column(DateTime, index = True)
    notes = Column(String)
    service = Column(String)



