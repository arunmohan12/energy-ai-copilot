from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.energy_bill import EnergyBill
from app.schemas.bill_extraction import EnergyBillExtraction

def save_bill_extraction(
        extraction: EnergyBillExtraction,
        db: Session,
) -> EnergyBill :
    bill = EnergyBill(
        customer_name=extraction.customer_name,
        billing_period_start=extraction.billing_period_start,
        billing_period_end=extraction.billing_period_end,
        due_date=extraction.due_date,
        electricity_meter_number=extraction.electricity_meter_number,
        previous_meter_reading=extraction.previous_meter_reading,
        current_meter_reading=extraction.current_meter_reading,
        energy_consumption=extraction.energy_consumption,
        electricity_charges=extraction.electricity_charges,
        water_charges=extraction.water_charges,
        service_charges=extraction.service_charges,
        vat=extraction.vat,
        total_amount=extraction.total_amount,
        payment_status=extraction.payment_status,
        status="validated"
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

def update_bill_extraction(db: Session,
        extraction: EnergyBillExtraction,
        bill: EnergyBill,customer: Customer)-> EnergyBill:
    bill.customer_name = extraction.customer_name
    bill.customer_id =customer.id

    bill.billing_period_start = extraction.billing_period_start
    bill.billing_period_end = extraction.billing_period_end
    bill.due_date = extraction.due_date
    bill.electricity_meter_number = extraction.electricity_meter_number
    bill.previous_meter_reading = extraction.previous_meter_reading
    bill.current_meter_reading = extraction.current_meter_reading
    bill.energy_consumption = extraction.energy_consumption
    bill.electricity_charges = extraction.electricity_charges
    bill.water_charges = extraction.water_charges
    bill.service_charges = extraction.service_charges
    bill.vat = extraction.vat
    bill.total_amount = extraction.total_amount
    bill.payment_status = extraction.payment_status
    bill.status = "validated"

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill

