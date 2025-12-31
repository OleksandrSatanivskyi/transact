from datetime import datetime, timezone
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.stock import StockTransaction, Stock
from src.schemas.transaction import TransactionCreate, TransactionUpdate


async def create(request: TransactionCreate, session: AsyncSession) -> StockTransaction:
    transaction = StockTransaction(
        stock_id=request.asset_id,
        price_per_one=request.price_per_one,
        amount=request.amount,
        total_price=request.price_per_one * request.amount,
        comment=request.comment,
        creation_date=request.creation_date or datetime.now(timezone.utc),
    )
    session.add(transaction)

    stmnt = select(Stock).where(Stock.id == transaction.stock_id)
    result = await session.execute(stmnt)
    stock = result.scalar_one()
    stock.amount += transaction.amount

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def update(id: NonNegativeInt, request: TransactionUpdate, session: AsyncSession) -> StockTransaction:
    transaction = await session.get(
        StockTransaction, id, options=[joinedload(StockTransaction.stock)]
    )

    if not transaction:
        raise ValueError(f"StockTransaction with id {id} doesn't exist")

    transaction.price_per_one = request.price_per_one

    transaction.stock.amount -= transaction.amount
    transaction.amount = request.amount
    transaction.stock.amount += request.amount

    transaction.stock.updation_date = datetime.now(timezone.utc)

    transaction.total_price = request.total_price
    transaction.comment = request.comment

    await session.commit()
    await session.refresh(transaction)
    return transaction


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    transaction = await session.get(
        StockTransaction, id, options=[joinedload(StockTransaction.stock)]
    )

    if not transaction:
        return False

    transaction.stock.amount -= transaction.amount
    transaction.stock.updation_date = datetime.now(timezone.utc)

    stmnt = delete(StockTransaction).where(StockTransaction.id == id)
    result = await session.execute(stmnt)
    await session.commit()
    return result.rowcount > 0


async def get_all_for_stock(stock_id: NonNegativeInt, session: AsyncSession) -> List[StockTransaction]:
    stmnt = (
        select(StockTransaction)
        .where(StockTransaction.stock_id == stock_id)
        .order_by(StockTransaction.creation_date)
    )
    result = await session.execute(stmnt)
    return result.scalars().all()


async def get_all(session: AsyncSession) -> List[StockTransaction]:
    stmnt = select(StockTransaction).order_by(StockTransaction.creation_date)
    result = await session.execute(stmnt)
    return result.scalars().all()

