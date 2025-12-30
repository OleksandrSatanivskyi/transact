import datetime

from sqlalchemy import Integer, String, DateTime, Numeric, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from src.database import Base


class Transaction(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price_per_one: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)

    __table_args__ = (
        CheckConstraint("price_per_one > 0", "price_per_one_positive"),
        CheckConstraint("amount > 0", "amount_positive"),
        CheckConstraint("total_price > 0", "total_price_positive"),
    )

class StockTransaction(Transaction):
    __tablename__ = "stock_transactions"
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"))
    stock: Mapped["Stock"] = relationship("Stock", back_populates="transactions")

class CryptoTransaction(Transaction):
    __tablename__ = "crypto_transactions"
    crypto_id: Mapped[int] = mapped_column(Integer, ForeignKey("cryptos.id"))
    crypto: Mapped["Crypto"] = relationship("Crypto", back_populates="transactions")