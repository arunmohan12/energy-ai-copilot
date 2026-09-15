import json
from pathlib import Path


from app.database import SessionLocal
from app.schemas.bill_extraction import EnergyBillExtraction
from app.ai.bill_validator import validate_bill
from app.services.bill_persistence import save_bill_extraction
from app.models.energy_bill import EnergyBill


def test_bill_persistence():
    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")

    with fixture_path.open() as file:
        data = json.load(file)

    extraction = EnergyBillExtraction.model_validate(data)

    validation_result = validate_bill(extraction)

    assert validation_result.valid is True

    db = SessionLocal()

    try:
        bill = save_bill_extraction(extraction,db)

        assert bill.id is not None
        assert bill.customer_name == "John Smith"
        assert bill.energy_consumption == extraction.energy_consumption
        assert bill.total_amount == extraction.total_amount
        assert bill.electricity_meter_number == "MTR-784512"
        assert bill.status == "validated"

    finally:
        db.delete(bill)
        db.commit()
        db.close()






