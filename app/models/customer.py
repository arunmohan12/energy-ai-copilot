from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    email: Mapped[str] = mapped_column(String(255),nullable=True,unique=True)
    mobile: Mapped[str] = mapped_column(String(20),nullable=True,unique=True)
    account_number: Mapped[str | None] = mapped_column(String(100),nullable=True,unique=True)

    bills = relationship("EnergyBill", back_populates="customer")



