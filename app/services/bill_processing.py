from sqlalchemy.orm import Session

from app.ai.bill_extractor import analyze_bill
from app.ai.bill_validator import validate_bill
from app.models.energy_bill import EnergyBill
from app.services.bill_persistence import update_bill_extraction
from app.services.energy_copilot import get_customer_number_by_account_number


def process_bill_extraction(
    db: Session,
    bill: EnergyBill,
) -> EnergyBill:

    extraction = analyze_bill(bill.file_path)

    validation_result = validate_bill(extraction)

    if not validation_result.valid:
        bill.status = "validation_failed"

        db.commit()
        db.refresh(bill)

        return bill
    if not extraction.account_number:
        bill.status = "customer_not_found"
        db.commit()
        db.refresh(bill)

        return bill

    customer = get_customer_number_by_account_number(db,extraction.account_number)

    if customer is None:
        bill.status = "customer_not_found"
        db.commit()
        db.refresh(bill)
        return bill

    return update_bill_extraction(
        db,
        extraction,
        bill,
        customer
    )