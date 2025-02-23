from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.settings import db_settings

ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_settings.connection_string}?"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
