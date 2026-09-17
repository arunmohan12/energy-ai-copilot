from app.services.energy_copilot import get_bill
from app.database import SessionLocal

def test_get_bill():
    db = SessionLocal()
    bill = get_bill(db,10)

    assert bill is not None
    assert bill.id == 10