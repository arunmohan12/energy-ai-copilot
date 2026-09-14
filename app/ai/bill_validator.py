from decimal import Decimal

from psycopg.types import none

from app.schemas.bill_extraction import EnergyBillExtraction

def validate_consumption(extraction: EnergyBillExtraction) -> bool:

    if(
        extraction.previous_meter_reading is none
        or extraction.current_meter_reading is none
        or extraction.energy_consumption is none
    ):
        return True

    calculated_consumption = (extraction.current_meter_reading - extraction.previous_meter_reading)

    return calculated_consumption == extraction.energy_consumption