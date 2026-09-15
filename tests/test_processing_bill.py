
import json
from pathlib import Path

from app.schemas.bill_extraction import EnergyBillExtraction
from app.database import SessionLocal
from app.models.energy_bill import EnergyBill
from unittest.mock import patch
from app.services.bill_processing import process_bill_extraction

def test_process_bill():
    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")
    with open(fixture_path) as f:
        fixture = json.load(f)

        extraction = EnergyBillExtraction.model_validate(fixture)


    db= SessionLocal()

    bill = EnergyBill(
        original_filename="sample-bill.pdf",
        stored_filename="test-file.pdf",
        file_path="data/raw/bills/test-file.pdf",
        content_type="application/pdf",
        status="uploaded",
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    try:
        with patch(
            "app.services.bill_processing.analyze_bill",
            return_value=extraction,
        ):
            processed_bill = process_bill_extraction(
                db,
                bill,
            )

        assert processed_bill.id == bill.id
        assert processed_bill.customer_name == "John Smith"
        assert processed_bill.energy_consumption == extraction.energy_consumption
        assert processed_bill.total_amount == extraction.total_amount
        assert processed_bill.status == "validated"

    finally:
        db.delete(bill)
        db.commit()
        db.close()

