from typing import List

from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.transaction import TransactionGet, TransactionCreate, TransactionUpdate
from src.services import transaction_service

transaction_router = APIRouter(prefix="/assets/transactions", tags=["asset_transactions"])

@transaction_router.post("/", response_model=TransactionGet)
async def create_transaction(request: TransactionCreate, session: AsyncSession = Depends(get_session)) -> TransactionGet:
    return await transaction_service.create(request, session)


@transaction_router.put("/{transaction_id}", response_model=TransactionGet)
async def update_transaction(transaction_id: NonNegativeInt, request: TransactionUpdate, session: AsyncSession = Depends(get_session)) -> TransactionGet:
    return await transaction_service.update(transaction_id, request, session)


@transaction_router.delete("/{transaction_id}", response_model=bool)
async def delete_transaction(transaction_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> bool:
    return await transaction_service.delete(transaction_id, session)


@transaction_router.get("/all/{asset_id}", response_model=List[TransactionGet])
async def get_all_for_asset(asset_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> List[TransactionGet]:
    return await transaction_service.get_all_for_asset(asset_id, session)


@transaction_router.get("/all", response_model=List[TransactionGet])
async def get_all_transactions(session: AsyncSession = Depends(get_session)) -> List[TransactionGet]:
    return await transaction_service.get_all(session)