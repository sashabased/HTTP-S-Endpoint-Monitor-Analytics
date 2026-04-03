from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

url = "postgresql+asyncpg://postgres:19762003@localhost/HTTPDashboardTools"

engine = create_async_engine(url)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)