from datetime import datetime
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.asset import Asset, Transaction
from src.schemas.transaction import TransactionCreate, TransactionUpdate


async def create(request: TransactionCreate, session: AsyncSession) -> Transaction:
    transaction = Transaction(
        asset_id=request.asset_id,
        price_per_one=request.price_per_one,
        amount=request.amount,
        total_price=request.price_per_one * request.amount,
        comment=request.comment,
        is_active=request.is_active,
        creation_date=request.creation_date or datetime.now(datetime.timezone.utc),
    )
    session.add(transaction)

    stmt = select(Asset).where(Asset.id == transaction.asset_id)
    result = await session.execute(stmt)
    asset = result.scalar_one()
    asset.amount += transaction.amount
    asset.updation_date = datetime.now(datetime.timezone.utc)

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def update(id: NonNegativeInt, request: TransactionUpdate, session: AsyncSession) -> Transaction:
    transaction = await session.get(Transaction, id, options=[joinedload(Transaction.asset)])
    if not transaction:
        raise ValueError(f"Transaction with id {id} doesn't exist")

    transaction.asset.amount -= transaction.amount

    transaction.price_per_one = request.price_per_one
    transaction.amount = request.amount
    transaction.total_price = request.price_per_one * request.amount
    transaction.comment = request.comment
    transaction.is_active = request.is_active
    transaction.asset.amount += request.amount
    transaction.asset.updation_date = datetime.now(datetime.timezone.utc)

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    transaction = await session.get(Transaction, id, options=[joinedload(Transaction.asset)])
    if not transaction:
        raise ValueError(f"Transaction with id {id} doesn't exist")

    transaction.asset.amount -= transaction.amount
    transaction.asset.updation_date = datetime.now(datetime.timezone.utc)

    stmt = delete(Transaction).where(Transaction.id == id)
    result = await session.execute(stmt)

    await session.commit()
    return result.rowcount > 0


async def get_all_for_asset(asset_id: NonNegativeInt, session: AsyncSession) -> List[Transaction]:
    stmt = (
        select(Transaction)
        .where(Transaction.asset_id == asset_id)
        .order_by(Transaction.creation_date)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_all(session: AsyncSession) -> List[Transaction]:
    stmt = select(Transaction).join(Transaction.asset).order_by(
        Transaction.creation_date,
        Transaction.asset.updation_date,
        Transaction.asset_id
    )
    result = await session.execute(stmt)
    return result.scalars().all()
