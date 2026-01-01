import datetime
from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.asset import Asset
from src.schemas.asset import AssetUpdate, AssetGet


async def create(request: AssetUpdate, session: AsyncSession) -> Asset:
    asset = Asset(
        **request.model_dump(),
        updation_date=datetime.datetime.now(datetime.timezone.utc),
        amount=0
    )
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    return asset


async def update(id: NonNegativeInt, request: AssetUpdate, session: AsyncSession) -> Asset:
    asset = await session.get(Asset, id)
    if not asset:
        raise ValueError(f"Asset with id {id} doesn't exist")

    asset.ticker = request.ticker
    asset.name = request.name
    asset.asset_type = request.asset_type
    asset.risk = request.risk
    asset.updation_date = datetime.datetime.now(datetime.timezone.utc)

    await session.commit()
    await session.refresh(asset)
    return asset


async def delete(id: NonNegativeInt, session: AsyncSession) -> bool:
    stmnt = delete(Asset).where(Asset.id == id)
    result = await session.execute(stmnt)
    await session.commit()
    return result.rowcount > 0


async def get(id: NonNegativeInt, session: AsyncSession) -> Asset:
    asset = await session.get(Asset, id)
    if not asset:
        raise ValueError(f"Asset with id {id} doesn't exist")
    return asset


async def get_all(session: AsyncSession) -> List[Asset]:
    stmnt = select(Asset)
    result = await session.execute(stmnt)
    return result.scalars().all()
