from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
import os

engine = create_async_engine(os.getenv("DATABASE_URL"))

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)