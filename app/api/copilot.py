from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.energy_copilot import get_bill, find_customers, resolve_customers, get_customer_bills, get_customer_latest_bills

router = APIRouter(
    prefix="/api/copilot",
    tags=["Energy Copilot"],
)

@router.get("/bills/{bill_id}")
def get_bill_for_copilot(
        bill_id: int,
        db: Session = Depends(get_db),
        ):

    bill = get_bill(db,bill_id)

    if bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {
        "id": bill.id,
        "customer_name": bill.customer_name,
        "billing_period_start": bill.billing_period_start,
        "billing_period_end": bill.billing_period_end,
        "energy_consumption": bill.energy_consumption,
        "total_amount": bill.total_amount,
        "status": bill.status,
    }

@router.get("/customers/search")
def search_customers(
        search_term: str,
        db: Session = Depends(get_db),
):
    customers = find_customers(db,search_term)
    if customers is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return [
        {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "mobile": customer.mobile,
        "account_number": customer.account_number,
        }
    for customer in customers
    ]

@router.get("/customers/resolve")
def resolve_customer_for_copilot(
    q: str,
    db: Session = Depends(get_db),
):
    result = resolve_customers(
        db,
        q,
    )

    if result.status == "not_found":
        return {
            "status": "not_found",
            "message": f"No customer found matching '{q}'.",
        }

    if result.status == "resolved":
        customer = result.customer

        return {
            "status": "resolved",
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "mobile": customer.mobile,
                "account_number": customer.account_number,
            },
        }

    return {
        "status": "ambiguous",
        "message": f"Multiple customers found matching '{q}'.",
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "mobile": customer.mobile,
                "account_number": customer.account_number,
            }
            for customer in result.customers
        ],
    }

@router.get("/customers/{customer_id}/bills")
def get_customer_bills_for_copilot(
        customer_id: int,
        db: Session = Depends(get_db),
):
    bills = get_customer_bills(db,customer_id)

    return [
        {
            "id": bill.id,
            "customer_id": bill.customer_id,
            "customer_name": bill.customer_name,
            "billing_period_start": bill.billing_period_start,
            "billing_period_end": bill.billing_period_end,
            "energy_consumption": bill.energy_consumption,
            "total_amount": bill.total_amount,
            "status": bill.status,
        }
        for bill in bills
    ]

@router.get("/customers/{customer_id}/latestbill")
def get_customer_latest_bill_for_copilot(
        customer_id: int,
        db: Session = Depends(get_db),
):
    bill = get_customer_latest_bills(db, customer_id)

    if bill is None:
        raise HTTPException(status_code=404, detail="Latest bill not found")

    return {
        "id": bill.id,
        "customer_id": bill.customer_id,
        "customer_name": bill.customer_name,
        "billing_period_start": bill.billing_period_start,
        "billing_period_end": bill.billing_period_end,
        "energy_consumption": bill.energy_consumption,
        "total_amount": bill.total_amount,
        "status": bill.status,
    }