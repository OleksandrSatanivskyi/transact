import datetime
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.crypto import Crypto
from src.schemas.asset import AssetUpdate, AssetGet


async def create(request: AssetUpdate, session: AsyncSession) -> Crypto:
    crypto = Crypto(**request.model_dump(), updation_date=datetime.now(datetime.timezone.utc), amount=0)
    session.add(crypto)
    await session.commit()
    await session.refresh(crypto)
    return crypto


async def update(id: NonNegativeInt, request: AssetUpdate, session: AsyncSession) -> Crypto:
    crypto = await session.get(Crypto, id)

    if not crypto:
        raise ValueError(f"Crypto with id {id} doesn't exist")

    crypto.ticker = request.ticker
    crypto.name = request.name
    crypto.updation_date = datetime.now(datetime.timezone.utc)

    await session.commit()
    await session.refresh(crypto)
    return crypto


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    stmnt = delete(Crypto).where(Crypto.id == id)
    result = await session.execute(stmnt)
    await session.commit()
    return result.rowcount > 0


async def get(id: NonNegativeInt, session: AsyncSession) -> Crypto:
    crypto = await session.get(Crypto, id)

    if not crypto:
        raise ValueError(f"Crypto with id {id} doesn't exist")

    return crypto


async def get_all(session: AsyncSession) -> List[Crypto]:
    stmnt = select(Crypto)
    result = await session.execute(stmnt)
    return result.scalars().all()
