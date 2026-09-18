import os
import json

from app.ai.gemini_client import client
from app.copilot.tools.customer import (
    SEARCH_CUSTOMER_TOOL,
    search_customers,
)
from app.database import SessionLocal


GEMINI_MODEL = os.getenv("GEMINI_MODEL")

TOOLS = [
    SEARCH_CUSTOMER_TOOL,
]


def chat(message: str) -> str:

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=message,
        tools=TOOLS,
    )

    for step in interaction.steps:

        if step.type != "function_call":
            continue

        if step.name == "search_customers":

            search_term = step.arguments["search_term"]

            db = SessionLocal()

            try:
                customers = search_customers(
                    db,
                    search_term,
                )

                result = [
                    {
                        "id": customer.id,
                        "name": customer.name,
                        "email": customer.email,
                        "mobile": customer.mobile,
                        "account_number": customer.account_number,
                    }
                    for customer in customers
                ]

            finally:
                db.close()

            final_interaction = client.interactions.create(
                model=GEMINI_MODEL,
                previous_interaction_id=interaction.id,
                tools=TOOLS,
                input=[
                    {
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result),
                            }
                        ],
                    }
                ],
            )

            return final_interaction.output_text

    return interaction.output_text


if __name__ == "__main__":

    result = chat(
        "show details of john"
    )

    print(result)