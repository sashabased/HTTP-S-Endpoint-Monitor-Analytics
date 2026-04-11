from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


class DBSessionManager:
    def __init__(self):
        self._engine = None
        self._session_maker = None

    
    def init(self, db_ulr: str):
        if self._engine is not None:
            raise RuntimeError("DBSessionManager already initialized")
        
        self._engine = create_async_engine(db_ulr, pool_pre_ping=True)
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False
        )

    
    async def close(self):
        if self._engine is None:
            return
        
        await self._engine.dispose()

        self._engine = None
        self._session_maker = None

    
    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        if self._session_maker is None:
            raise RuntimeError("DBSessionManager is not initialized")
        return self._session_maker


db_manager = DBSessionManager()