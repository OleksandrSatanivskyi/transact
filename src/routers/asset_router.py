from typing import List

from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.asset import AssetGet, AssetUpdate
from src.services import asset_service


asset_router = APIRouter(prefix="/assets", tags=["assets"])

@asset_router.get("/{asset_id}", response_model=AssetGet)
async def get_asset(asset_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> AssetGet:
    return await asset_service.get(asset_id, session)


@asset_router.post("/", response_model=AssetGet)
async def create_asset(request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    return await asset_service.create(request, session)


@asset_router.put("/{asset_id}", response_model=AssetGet)
async def update_asset(asset_id: NonNegativeInt, request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    return await asset_service.update(asset_id, request, session)


@asset_router.delete("/{asset_id}", response_model=bool)
async def delete_asset(asset_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> bool:
    return await asset_service.delete(asset_id, session)


@asset_router.get("/all", response_model=List[AssetGet])
async def get_all_assets(session: AsyncSession = Depends(get_session)) -> List[AssetGet]:
    return await asset_service.get_all(session)