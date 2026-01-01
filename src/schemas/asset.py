from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, Field, ConfigDict, NonNegativeFloat

from src.models.asset import AssetType, Risk


class AssetUpdate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(..., min_length=1)
    asset_type: AssetType = Field(...)
    risk: Optional[Risk] = None

class AssetGet(BaseModel):
    id: NonNegativeInt = Field(...)
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(...)
    updation_date: datetime = Field(...)
    amount: NonNegativeFloat = Field(...)
    asset_type: AssetType = Field(...)
    risk: Optional[Risk] = None

    model_config = ConfigDict(from_attributes=True)

