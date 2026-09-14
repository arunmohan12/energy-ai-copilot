
from app.schemas.bill_extraction import EnergyBillExtraction
from app.schemas.validation import BillValidationResult

def validate_consumption(extraction: EnergyBillExtraction) -> str | None:

    if(
        extraction.previous_meter_reading is None
        or extraction.current_meter_reading is None
        or extraction.energy_consumption is None
    ):
        return None

    calculated_consumption = (extraction.current_meter_reading - extraction.previous_meter_reading)

    if calculated_consumption != extraction.energy_consumption:
        return (
            "Energy consumption does not match the difference "
            "between previous and current meter readings."
        )
    return None


def validate_total_amount(extraction: EnergyBillExtraction) -> str | None:
    charges=[extraction.electricity_charges,extraction.water_charges,extraction.service_charges,extraction.vat]

    if extraction.total_amount is None:
        return None
    if any(charge is None for charge in charges):
        return None

    calculated_charges = sum(charges)

    if calculated_charges != extraction.total_amount:
        return (
            "Total amount does not match the sum of "
            "electricity, water, service, and VAT charges."
        )
    return None


def validate_bill(extraction: EnergyBillExtraction) -> BillValidationResult:
    errors = []

    consumption_error = validate_consumption(extraction)
    if consumption_error:
        errors.append(consumption_error)

    total_amount_error = validate_total_amount(extraction)

    if total_amount_error:
        errors.append(total_amount_error)

    return BillValidationResult(
        valid=len(errors) == 0,
        errors=errors,
    )

