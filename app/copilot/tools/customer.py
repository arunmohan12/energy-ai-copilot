from sqlalchemy.orm import Session

from app.services.energy_copilot import find_customers

SEARCH_CUSTOMER_TOOL = {
    "type":"function",
    "name":"search_customers",
    "description":(
        "Search for customers using "
        "name,email,mobile number, account number, or customer id"
    ),
    "parameters":
        {
            "type":"object",
            "properties":{
                "search_term":{
                    "type":"string",
                    "description":(
                        "The customer's name, email, mobile number,account number or customer id "
                    ),
                },
            },
            "required":["search_term"],
        }

}

def search_customers(db: Session,search_term: str):
    return find_customers(db=db, search_term=search_term)