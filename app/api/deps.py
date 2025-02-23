from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session


async def database_session(
    async_session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[AsyncSession, None]:
    try:
        yield async_session
        await async_session.commit()
    except Exception:
        await async_session.rollback()
        raise
