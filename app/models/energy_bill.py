from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EnergyBill(Base):
    __tablename__ = "energy_bills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    customer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    billing_period_start: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    billing_period_end: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    due_date: Mapped[date| None] = mapped_column(
        Date,
        nullable=True,
    )

    electricity_meter_number: Mapped [str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    previous_meter_reading: Mapped [Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True,
    )

    current_meter_reading: Mapped [Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True
    )

    energy_consumption: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True,
    )

    electricity_charges: Mapped [Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )


    water_charges: Mapped [Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True
    )

    service_charges: Mapped [Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True
    )

    vat: Mapped[Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True,
    )

    total_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    payment_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )


    original_filename: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    stored_filename: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="uploaded",
        nullable=False,
    )