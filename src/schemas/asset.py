from datetime import datetime

from pydantic import BaseModel, NonNegativeInt, Field, ConfigDict, NonNegativeFloat


class AssetUpdate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(..., min_length=1)

class AssetGet(BaseModel):
    id: NonNegativeInt = Field(...)
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(...)
    updation_date: datetime = Field(...)
    amount: NonNegativeFloat = Field(...)

    model_config = ConfigDict(from_attributes=True)

