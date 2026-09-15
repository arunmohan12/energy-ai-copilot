import json
from pathlib import Path

from app.ai.bill_validator import validate_bill
from app.schemas.bill_extraction import EnergyBillExtraction
from app.database import SessionLocal
from app.models.energy_bill import EnergyBill
from app.services.bill_persistence import update_bill_extraction

def test_bill_update_with_extraction():


    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")
    with fixture_path.open() as file:
        data = json.load(file)

        extraction = EnergyBillExtraction.model_validate(data)

        validation_result = validate_bill(extraction)

        assert validation_result.valid is True

        db=SessionLocal()

        bill = EnergyBill(
            original_filename="sample-bill.pdf",
            stored_filename = "test-file.pdf",
            file_path="data/raw/bills/test-file.pdf",
            content_type="application/pdf",
            status="uploaded",
        )

        db.add(bill)
        db.commit()
        db.refresh(bill)

    try:
        updated_bill = update_bill_extraction(db,extraction,bill)

        assert updated_bill.id == bill.id
        assert updated_bill.customer_name == "John Smith"
        assert updated_bill.billing_period_start == extraction.billing_period_start
        assert updated_bill.billing_period_end == extraction.billing_period_end
        assert updated_bill.due_date == extraction.due_date
        assert updated_bill.electricity_meter_number == "MTR-784512"
        assert updated_bill.previous_meter_reading == extraction.previous_meter_reading
        assert updated_bill.current_meter_reading == extraction.current_meter_reading
        assert updated_bill.energy_consumption == extraction.energy_consumption
        assert updated_bill.electricity_charges == extraction.electricity_charges
        assert updated_bill.water_charges == extraction.water_charges
        assert updated_bill.service_charges == extraction.service_charges
        assert updated_bill.vat == extraction.vat
        assert updated_bill.total_amount == extraction.total_amount
        assert updated_bill.payment_status == "UNPAID"
        assert updated_bill.status == "validated"

    finally:
        db.delete(bill)
        db.commit()
        db.close()
