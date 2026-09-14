import json
from pathlib import Path

from app.ai.bill_validator import validate_bill
from app.schemas.bill_extraction import EnergyBillExtraction


def test_sample_bill_validation():
    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")

    with fixture_path.open() as file:
        data = json.load(file)

    extraction = EnergyBillExtraction.model_validate(data)

    result = validate_bill(extraction)
    assert result.valid is True
    assert result.errors == []


def test_invalid_consumption_is_rejected():
    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")
    with fixture_path.open() as file:
        data = json.load(file)

        data["energy_consumption"] = "1300"

        extraction = EnergyBillExtraction.model_validate(data)

        result = validate_bill(extraction)
        assert result.valid is False
        assert "Energy consumption does not match" in result.errors[0]

def test_invalid_total_amount_is_rejected():
    fixture_path = Path("tests/fixtures/sample_energy_bill_extraction.json")
    with fixture_path.open() as file:
        data = json.load(file)

        data["total_amount"] = "300.00"

        extraction = EnergyBillExtraction.model_validate(data)
        result= validate_bill(extraction)
        assert result.valid is False
        assert "Total amount does not match" in result.errors[0]


