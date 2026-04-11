from app.database.session import db_manager
from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = db_manager.get_session_maker()
    async with session_maker() as session:
        yield session