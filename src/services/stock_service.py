import datetime
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.stock import Stock
from src.schemas.asset import AssetUpdate, AssetGet


async def create(request: AssetUpdate, session: AsyncSession) -> Stock:
    stock = Stock(**request.model_dump(), updation_date = datetime.now(datetime.timezone.utc), amount=0)
    session.add(stock)
    await session.commit()
    await session.refresh(stock)
    return stock


async def update(id: NonNegativeInt, request: AssetUpdate, session: AsyncSession) -> Stock:
    stock = await session.get(Stock, id)

    if not stock:
        raise ValueError(f"Stock with id {id} doesn't exist")

    stock.ticker = request.ticker
    stock.name = request.name
    stock.updation_date = datetime.now(datetime.timezone.utc)

    await session.commit()
    await session.refresh(stock)
    return stock


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    stmnt = delete(Stock, id).where(Stock.id == id)
    result = await session.execute(stmnt)
    await session.commit()
    return result.rowcount > 0


async def get(id: NonNegativeInt, session: AsyncSession) -> Stock:
    stock = await session.get(Stock, id)

    if not stock:
        raise ValueError(f"Stock with id {id} doesn't exist")

    return stock


async def get_all(session: AsyncSession) -> List[Stock]:
    stmnt = select(Stock)
    result = await session.execute(stmnt)
    return result.scalars().all()
