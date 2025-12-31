from typing import List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.asset import Asset, Transaction


class CryptoTransaction(Transaction):
    __tablename__ = "crypto_transactions"
    crypto_id: Mapped[int] = mapped_column(Integer, ForeignKey("cryptos.id"))
    crypto: Mapped["Crypto"] = relationship("Crypto", back_populates="transactions")

class Crypto(Asset):
    __tablename__ = "cryptos"
    transactions: Mapped[List["CryptoTransaction"]] = relationship("CryptoTransaction", back_populates="crypto")