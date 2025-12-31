from typing import List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.asset import Asset, Transaction


class StockTransaction(Transaction):
    __tablename__ = "stock_transactions"
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"))
    stock: Mapped["Stock"] = relationship("Stock", back_populates="transactions")


class Stock(Asset):
    __tablename__ = "stocks"
    transactions: Mapped[List["StockTransaction"]] = relationship("StockTransaction", back_populates="stock")
