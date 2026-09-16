from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class EnergyBillCreate(BaseModel):
    customer_name: str | None = None

    billing_period_start: date | None = None
    billing_period_end: date | None = None

    total_amount: Decimal | None = None
    energy_consumption: Decimal | None = None


class EnergyBillResponse(BaseModel):
    id: int
    customer_name: str | None = None
    billing_period_start: date | None = None
    billing_period_end: date | None = None
    total_amount: Decimal | None = None
    energy_consumption: Decimal | None = None
    status: str

    model_config = {
        "from_attributes": True
    }