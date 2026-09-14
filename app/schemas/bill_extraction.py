from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class EnergyBillExtraction(BaseModel):
    customer_name: str | None = None

    billing_period_start: date | None = None
    billing_period_end: date | None = None
    due_date: date | None = None

    electricity_meter_number: str | None = None
    previous_meter_reading: Decimal | None = None
    current_meter_reading: Decimal | None = None
    energy_consumption: Decimal | None = None

    electricity_charges: Decimal | None = None
    water_charges: Decimal | None = None
    service_charges: Decimal | None = None
    vat: Decimal | None = None
    total_amount: Decimal | None = None

    payment_status: str | None = None