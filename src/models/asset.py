from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Asset(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    updation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(ticker) > 0 AND LENGTH(ticker) < 8", "ticker_length"),
    )

class Stock(Asset):
    __tablename__ = "stocks"
    transactions: Mapped[List["StockTransaction"]] = relationship("StockTransaction", back_populates="stock")

class Crypto(Asset):
    __tablename__ = "cryptos"
    transactions: Mapped[List["CryptoTransaction"]] = relationship("CryptoTransaction", back_populates="crypto")