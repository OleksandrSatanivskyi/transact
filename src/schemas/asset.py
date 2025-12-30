from datetime import datetime

from pydantic import BaseModel, NonNegativeInt, Field


class AssetCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(...)

class AssetGet(BaseModel):
    id: int = Field(...)
    ticker: str = Field(..., min_length=1, max_length=8)
    name: str = Field(...)
    updation_date: datetime = Field(...)

    class Config:
        orm_mode = True

