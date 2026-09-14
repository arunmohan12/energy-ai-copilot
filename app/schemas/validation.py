from pydantic import BaseModel


class BillValidationResult(BaseModel):
    valid: bool
    errors: list[str] = []