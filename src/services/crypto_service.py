from sqlalchemy.ext.asyncio import AsyncSession

from src.models.asset import Crypto
from src.schemas.asset import AssetCreate, AssetGet


async def create(request: AssetCreate, db: AsyncSession) -> AssetGet:
    crypto = Crypto()