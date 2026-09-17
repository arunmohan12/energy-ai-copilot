from sqlalchemy import or_

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.energy_bill import EnergyBill
from dataclasses import dataclass
from datetime import date


@dataclass
class CustomerResolution:
    status: str
    customer: Customer | None = None
    customers: list[Customer] | None = None

@dataclass
class BillComparison:
    bill_1: EnergyBill
    bill_2: EnergyBill
    consumption_change: float
    consumption_change_percent: float | None
    amount_change: float
    amount_change_percent: float | None

def get_bill(db: Session, bill_id: int) -> EnergyBill | None:
    return db.get(EnergyBill, bill_id)


def get_customer_bills(
    db: Session,
    customer_id: int,
) -> list[EnergyBill]:
    return (
        db.query(EnergyBill)
        .filter(EnergyBill.customer_id == customer_id)
        .order_by(EnergyBill.billing_period_end.desc())
        .all()
    )


def get_customer_latest_bills(
    db: Session,
    customer_id: int,
) -> EnergyBill | None:
    return (
        db.query(EnergyBill)
        .filter(EnergyBill.customer_id == customer_id)
        .order_by(EnergyBill.billing_period_end.desc())
        .first()
    )



def find_customers(db: Session,search_term: str,) -> list[Customer]:
    search_term = search_term.strip()

    conditions = [
        Customer.name.ilike(f"%{search_term}%"),
        Customer.email == search_term,
        Customer.mobile == search_term,
        Customer.account_number == search_term,
    ]
    if search_term.isdigit():
        conditions.append(
            Customer.id == int(search_term)
        )

    return (db.query(Customer).filter(or_(*conditions)).all()
            )

def resolve_customers(db: Session, search_term: str) -> CustomerResolution:
    customers = find_customers(db, search_term)
    if not customers:
        return CustomerResolution(status="not_found", customer=None)
    if len(customers) == 1:
        return CustomerResolution(status="resolved", customer=customers[0])
    return CustomerResolution(status="ambiguous", customers=customers)

def find_bill_by_period(db: Session,customer_id: int,year: int,month: int) -> EnergyBill | None:
    period_start = date(year=year, month=month, day=1)

    return (
        db.query(EnergyBill)
            .filter(
                    EnergyBill.customer_id == customer_id,
                    EnergyBill.billing_period_start == period_start,
                    )
            .first()

            )

def compare_bills(
    db: Session,
    customer_id: int,
    year_1: int,
    month_1: int,
    year_2: int,
    month_2: int,
) -> BillComparison | None:
    bill_1 = find_bill_by_period(
        db,
        customer_id,
        year_1,
        month_1,
    )

    bill_2 = find_bill_by_period(
        db,
        customer_id,
        year_2,
        month_2,
    )

    if bill_1 is None or bill_2 is None:
        return None

    consumption_change = (
        float(bill_2.energy_consumption)
        - float(bill_1.energy_consumption)
    )

    amount_change = (
        float(bill_2.total_amount)
        - float(bill_1.total_amount)
    )

    consumption_change_percent = None

    if bill_1.energy_consumption:
        consumption_change_percent = (
            consumption_change
            / float(bill_1.energy_consumption)
        ) * 100

    amount_change_percent = None

    if bill_1.total_amount:
        amount_change_percent = (
            amount_change
            / float(bill_1.total_amount)
        ) * 100

    return BillComparison(
        bill_1=bill_1,
        bill_2=bill_2,
        consumption_change=consumption_change,
        consumption_change_percent=consumption_change_percent,
        amount_change=amount_change,
        amount_change_percent=amount_change_percent,
    )


def get_customer_number_by_account_number(
    db: Session,
    account_no: str,
)-> Customer | None:
    return (
        db.query(Customer)
        .filter(Customer.account_number == account_no)
        .first()
    )
