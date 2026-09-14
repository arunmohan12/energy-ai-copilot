from pathlib import Path
from app.ai.gemini_client import client, interaction
from app.schemas.bill_extraction import EnergyBillExtraction


def analyze_bill(pdf_path:str) -> EnergyBillExtraction:
    file_path = Path(pdf_path)

    uploaded_file  = client.files.upload(
        file=file_path,
    )

    prompt = """ 
    Analyze this energy bill carefully.

Identify all useful information you can find, including:
- customer information
- account or bill number
- billing period
- electricity consumption
- previous and current meter readings
- electricity charges
- water charges
- service charges
- taxes or VAT
- total amount
- payment status
- due date
- any other relevant energy-related information

Do not guess information that is not present in the document.

Return your findings in clear text.
    """

    interaction = client.interactions.create(

        model="gemini-3.6-flash",
        input=[
            {"type": "text","text": prompt},
            {"type":"document","uri":uploaded_file.uri, "mimetype":uploaded_file.mime_type},

        ],
        response_format=[
            {
                         "type": "text",
                         "mime_type":"application/json",
                         "schema":EnergyBillExtraction.model_json_schema(),
                         }
            ],
    )

    return EnergyBillExtraction.model_validate_json(interaction.output_text)