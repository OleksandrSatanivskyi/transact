from datetime import datetime, timezone

from pydantic import NonNegativeFloat, NonNegativeInt
from sqlalchemy import Integer, String, CheckConstraint, DateTime, Numeric, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from enum import StrEnum


class AssetType(StrEnum):
    STOCK = "stock"
    CRYPTO = "crypto"
    GOLD = "gold"
    CASH = "cash"


class Risk(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[NonNegativeInt] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    updation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    amount: Mapped[NonNegativeFloat] = mapped_column(Numeric(18, 8), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType, native_enum=False), nullable=False)
    risk: Mapped[Risk] = mapped_column(Enum(Risk, native_enum=False), nullable=True)
    transactions: Mapped["Transaction"] = relationship("Transaction", back_populates="asset")


    __table_args__ = (
        CheckConstraint("LENGTH(ticker) > 0 AND LENGTH(ticker) < 8", "ticker_length"),
        CheckConstraint("amount >= 0", "amount_non_negative"),
    )