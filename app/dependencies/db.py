from app.database.session import db_manager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastapi import Depends

from typing import AsyncGenerator, Annotated

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker: async_sessionmaker[AsyncSession] = db_manager.get_session_maker()
    async with session_maker() as session:
        yield session

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]