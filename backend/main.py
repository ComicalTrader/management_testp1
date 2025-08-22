from fastapi import FastAPI
from .database import Base,engine
from .routers import appointment
Base.metadata.create_all(bind= engine)
app = FastAPI(title="management API")



@app.get("/")
@app.get("/h")
def health(): 
    return{"status": "good"}


@app.get("/appointment")
def list_appointments():
    return {"appointments": []}