from itertools import count

from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies import get_db

app = FastAPI(title="EnergyAI Copilot")
@app.get("/")
def home():
    return {     "message": "EnergyAI Copilot API is running"}
@app.get("/ping")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT count(*) FROM energy_bills"))
    count = result.scalar()
    return {"energy_bills_count": count}