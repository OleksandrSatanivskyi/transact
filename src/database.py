from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

async_engine = create_async_engine(
    url=settings.DB_URL_asyncpg,
    echo=True,
)

SessionLocal = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with SessionLocal() as session:
        yield session