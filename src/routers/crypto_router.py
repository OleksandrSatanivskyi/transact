from typing import List

from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession
import src.services.crypto_service as crypto_service
from src.database import get_session
from src.schemas.asset import AssetGet, AssetUpdate

router = APIRouter(prefix="/crypto", tags=["crypto"])

@router.get(path="/{crypto_id}", response_model=AssetGet)
async def get_crypto(crypto_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await crypto_service.get(crypto_id, session)
    return result

@router.post(path="/", response_model=AssetGet)
async def create_crypto(request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await crypto_service.create(request, session)
    return result

@router.put(path="/{crypto_id}", response_model=AssetGet)
async def update_crypto(crypto_id: NonNegativeInt, request: AssetUpdate, session: AsyncSession = Depends(get_session)) -> AssetGet:
    result = await crypto_service.update(crypto_id, request, session)
    return result

@router.delete(path="/", response_model=bool)
async def delete_crypto(crypto_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> bool:
    result = await crypto_service.delete(crypto_id, session)
    return result

@router.get(path="/all", response_model=List[AssetGet])
async def get_all_cryptos(session: AsyncSession = Depends(get_session)) -> List[AssetGet]:
    result = await crypto_service.get_all(session)
    return result