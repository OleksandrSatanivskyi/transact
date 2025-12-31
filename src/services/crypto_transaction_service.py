from datetime import datetime
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.crypto import CryptoTransaction, Crypto
from src.schemas.transaction import TransactionUpdate, TransactionCreate


async def create(request: TransactionCreate, session: AsyncSession) -> CryptoTransaction:
    transaction = CryptoTransaction(
        crypto_id=request.stock_id,
        price_per_one=request.price_per_one,
        amount=request.amount,
        total_price=request.price_per_one * request.amount,
        comment=request.comment,
        creation_date=request.creation_date or datetime.now(datetime.timezone.utc),
    )
    session.add(transaction)

    stmnt = select(Crypto).where(
        Crypto.id == transaction.crypto_id
    )

    result = await session.execute(stmnt)
    crypto = result.scalar_one()
    crypto.amount += transaction.amount

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def update(id: NonNegativeInt, request: TransactionUpdate, session: AsyncSession) -> CryptoTransaction:
    transaction = await session.get(CryptoTransaction, id, options=[joinedload(CryptoTransaction.crypto)])

    if not transaction:
        raise ValueError(f"Transaction with id {id} doesn't exist")

    transaction.price_per_one = request.price_per_one

    transaction.crypto.amount -= transaction.amount
    transaction.amount = request.amount
    transaction.crypto.amount += request.amount

    transaction.crypto.updation_date = datetime.now(datetime.timezone.utc)

    transaction.total_price = request.total_price
    transaction.comment = request.comment

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    transaction = await session.get(CryptoTransaction, id, options=[joinedload(CryptoTransaction.crypto)])

    transaction.crypto.amount -= transaction.amount
    transaction.crypto.updation_date = datetime.now(datetime.timezone.utc)

    stmnt = delete(CryptoTransaction).where(CryptoTransaction.id == id)
    result = await session.execute(stmnt)

    await session.commit()
    return result.rowcount > 0


async def get_all_for_crypto(crypto_id: NonNegativeInt, session: AsyncSession) -> List[CryptoTransaction]:
    stmnt = (select(CryptoTransaction)
             .where(CryptoTransaction.crypto_id == crypto_id)
             .order_by(CryptoTransaction.creation_date)
    )
    result = await session.execute(stmnt)

    return result.scalars().all()


async def get_all(session: AsyncSession) -> List[CryptoTransaction]:
    stmnt = select(CryptoTransaction).order_by(CryptoTransaction.creation_date)
    result = await session.execute(stmnt)
    return result.scalars().all()