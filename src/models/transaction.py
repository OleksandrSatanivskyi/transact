from datetime import datetime, timezone

from pydantic import NonNegativeFloat, NonNegativeInt
from sqlalchemy import Integer, String, CheckConstraint, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[NonNegativeInt] = mapped_column(Integer, primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    price_per_one: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    amount: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    total_price: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    comment: Mapped[str|None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    asset_id: Mapped[NonNegativeInt] = mapped_column(Integer, ForeignKey("assets.id"))
    asset: Mapped["Asset"] = relationship("Asset", back_populates="transactions")


    __table_args__ = (
        CheckConstraint("price_per_one > 0", "price_per_one_positive"),
        CheckConstraint("amount > 0", "amount_positive"),
        CheckConstraint("total_price > 0", "total_price_positive"),
    )