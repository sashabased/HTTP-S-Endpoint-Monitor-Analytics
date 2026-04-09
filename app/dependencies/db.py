from app.database.session import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session