from datetime import datetime, timezone

from pydantic import NonNegativeFloat
from sqlalchemy import Integer, String, CheckConstraint, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Asset(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    updation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    amount: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(ticker) > 0 AND LENGTH(ticker) < 8", "ticker_length"),
    )


class Transaction(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    price_per_one: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    amount: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    total_price: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    comment: Mapped[str|None] = mapped_column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("price_per_one > 0", "price_per_one_positive"),
        CheckConstraint("amount > 0", "amount_positive"),
        CheckConstraint("total_price > 0", "total_price_positive"),
    )