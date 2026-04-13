from app.database.session import db_manager

from app.repository.endp_monitoring_repo import CheckResultRepository
from app.repository.sites_repo import SiteRepository
from app.repository.endpoints_repo import EndpointRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = db_manager.get_session_maker()


    async def __aenter__(self):
        self.session = self.session_factory()

        self.sites = SiteRepository(self.session)
        self.endpoints = EndpointRepository(self.session)
        self.check_results = CheckResultRepository(self.session)
        return self
    

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()