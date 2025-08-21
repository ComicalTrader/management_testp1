from fastapi import FastAPI
app = FastAPI("title= management API")


app.get("/health")
def health(): return{"status": "good"}

