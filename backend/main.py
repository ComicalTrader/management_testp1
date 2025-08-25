from fastapi import FastAPI
from .database import Base,engine
from .routers import appointment
from .routers import customers
from .routers import finance


Base.metadata.create_all(bind= engine)
app = FastAPI(title="management API")

app.include_router(appointment.router)
app.include_router(customers.router)
app.include_router(finance.router)




@app.get("/")
@app.get("/h")
async def health(): 
    return{"message": "Hello World"}


@app.get("/appointment")
def list_appointments():
    return {"appointments": []}