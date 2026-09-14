from datetime import date
from decimal import Decimal

from pydantic import BaseModel

class EnergyBillCreate(BaseModel):
    customer_name: str
    billing_period_start: date
    billing_period_end: date
    total_amount: Decimal
    energy_consumption: Decimal

class EnergyBillResponse(BaseModel):
        id: int
        customer_name: str
        billing_period_start: date
        billing_period_end: date
        total_amount: Decimal
        energy_consumption: Decimal

        model_config = {
            "from_attributes": True
        }
