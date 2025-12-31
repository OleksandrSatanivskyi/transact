from typing import List

from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.asset import AssetGet, AssetUpdate
import src.services.stock_service as stock_service

router = APIRouter(prefix="/stock", tags=["asset"])

@router.get(path="/{stock_id}", response_model=AssetGet)
async def get_stock(stock_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await stock_service.get(stock_id, session)
    return result

@router.post(path="/", response_model=AssetGet)
async def create_stock(request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await stock_service.create(request, session)
    return result

@router.put(path="/{stock_id}", response_model=AssetGet)
async def update_stock(stock_id: NonNegativeInt, request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await stock_service.update(stock_id, request, session)
    return result

@router.delete(path="/", response_model=bool)
async def delete_stock(stock_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> bool:
    result = await stock_service.delete(stock_id, session)
    return result

@router.get(path="/all", response_model=List[AssetGet])
async def get_all_stocks(session: AsyncSession = Depends(get_session)) -> List[AssetGet]:
    result = await stock_service.get_all(session)
    return result