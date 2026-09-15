import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.dependencies import get_db
from app.models.energy_bill import EnergyBill
from app.schemas.energy_bill import EnergyBillCreate, EnergyBillResponse
from app.services.bill_processing import process_bill_extraction
app = FastAPI(title="EnergyAI Copilot")
@app.get("/")
def home():
    return {     "message": "EnergyAI Copilot API is running"}
@app.get("/ping")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT count(*) FROM energy_bills"))
    count = result.scalar()
    return {"energy_bills_count": count}

@app.post("/api/billing")
def create_bill(bill:EnergyBillCreate, db: Session = Depends(get_db)):
    new_bill = EnergyBill(
        customer_name=bill.customer_name,
        billing_period_start=bill.billing_period_start,
        billing_period_end=bill.billing_period_end,
        total_amount=bill.total_amount,
        energy_consumption=bill.energy_consumption,
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return {
        "id" : new_bill.id,
        "customer_name" : new_bill.customer_name,
        "billing_period_start" : new_bill.billing_period_start,
        "billing_period_end" : new_bill.billing_period_end,
        "total_amount" : new_bill.total_amount,
        "energy_consumption" : new_bill.energy_consumption,
    }

@app.get("/api/bills", response_model=list[EnergyBillResponse])
def get_bills(db: Session = Depends(get_db)):
    bills = db.query(EnergyBill).all()

    return bills

@app.get("/api/bills/{id}", response_model=EnergyBillResponse)
def get_bill(id: int, db: Session = Depends(get_db)):
    bill = db.query(EnergyBill).filter(EnergyBill.id == id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@app.post("/api/bills/upload")
async def upload_bill(file : UploadFile = File(...),db: Session = Depends(get_db)):
    allowed_types = {
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPEG, and PNG files are allowed",
        )

    storage_directory = Path("data/raw/bills")
    storage_directory.mkdir(parents=True, exist_ok=True)

    file_extension = allowed_types[file.content_type]
    stored_filename = f"{uuid4()}{file_extension}"
    stored_path = storage_directory / stored_filename

    with stored_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_bill = EnergyBill(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(stored_path),
        content_type=file.content_type,
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return {
             "bill_id": new_bill.id,
        "original_filename": new_bill.original_filename,
        "stored_filename": new_bill.stored_filename,
        "file_path": new_bill.file_path,
        "content_type": new_bill.content_type,
        "status": new_bill.status,
    }

@app.post("/api/bills/{bill_id}/process")
def process_bill_api(bill_id: int, db: Session = Depends(get_db)):
    bill = db.get(EnergyBill,bill_id)
    if bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    processed_bill= process_bill_extraction(db,bill)

    return {
        "bill_id": processed_bill.id,
        "status": processed_bill.status,
        "customer_name": processed_bill.customer_name,
        "energy_consumption": processed_bill.energy_consumption,
        "total_amount": processed_bill.total_amount,
    }