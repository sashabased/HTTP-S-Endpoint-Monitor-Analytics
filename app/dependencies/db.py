from app.database.session import session_maker

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator:
    async with session_maker() as session:
        yield session