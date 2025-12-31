from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeFloat, Field, NonNegativeInt


class TransactionUpdate(BaseModel):
    creation_date: Optional[datetime] = None
    price_per_one: NonNegativeFloat = Field(...)
    amount: NonNegativeFloat = Field(...)
    total_price: NonNegativeFloat = Field(...)
    comment: Optional[str] = None

class TransactionCreate(BaseModel):
    asset_id: NonNegativeInt = Field(...)
    creation_date: Optional[datetime] = None
    price_per_one: NonNegativeFloat = Field(...)
    amount: NonNegativeFloat = Field(...)
    total_price: NonNegativeFloat = Field(...)
    comment: Optional[str] = None

class TransactionGet(BaseModel):
    id: NonNegativeInt = Field(...)
    creation_date: Optional[datetime] = None
    price_per_one: NonNegativeFloat = Field(...)
    amount: NonNegativeFloat = Field(...)
    total_price: NonNegativeFloat = Field(...)
    comment: Optional[str] = None
    asset_id: NonNegativeInt = Field(...)

    class Config:
        from_attributes = True