from typing import List

from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
import src.services.stock_transaction_service as stock_service
from src.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionGet

router = APIRouter(prefix="/stock/transactions", tags=["stock_transactions"])


@router.post("/", response_model=TransactionGet)
async def create_transaction(request: TransactionCreate, session: AsyncSession = Depends(get_session)) -> TransactionGet:
    return await stock_service.create(request, session)


@router.put("/{transaction_id}", response_model=TransactionGet)
async def update_transaction(transaction_id: NonNegativeInt, request: TransactionUpdate, session: AsyncSession = Depends(get_session)) -> TransactionGet:
    return await stock_service.update(transaction_id, request, session)


@router.delete("/{transaction_id}", response_model=bool)
async def delete_transaction(transaction_id: NonNegativeInt, session: AsyncSession = Depends(get_session)) -> bool:
    return await stock_service.delete(transaction_id, session)


@router.get("/all/{stock_id}", response_model=List[TransactionGet])
async def get_all_for_stock(stock_id: NonNegativeInt, session: AsyncSession = Depends(get_session)):
    return await stock_service.get_all_for_stock(stock_id, session)

@router.get("/all", response_model=List[TransactionGet])
async def get_all(session: AsyncSession = Depends(get_session)):
    return await stock_service.get_all(session)

