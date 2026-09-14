from app.ai.bill_extractor import analyze_bill
from app.ai.bill_validator import validate_bill
pdf_path = "data/raw/bills/0785def8-0ac4-4d87-9c30-72cb61034ed2.pdf"
result = analyze_bill(pdf_path)

print("\n===== STRUCTURED BILL EXTRACTION =====\n")
print(result.model_dump_json(indent=2))

validation_result = validate_bill(result)

print("\n===== BILL VALIDATION =====\n")
print(f"Validation passed: {validation_result.valid}")
print(f"Validation errors: {validation_result.errors}")