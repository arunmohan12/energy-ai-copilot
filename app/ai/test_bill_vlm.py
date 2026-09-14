from app.ai.bill_extractor import analyze_bill

pdf_path = "data/raw/bills/0785def8-0ac4-4d87-9c30-72cb61034ed2.pdf"
result = analyze_bill(pdf_path)

print("\n===== GEMINI BILL ANALYSIS =====\n")
print(result.model_dump_json(indent=2))