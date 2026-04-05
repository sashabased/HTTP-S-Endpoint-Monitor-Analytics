from fastapi import Depends

# monitoring
from app.repository.endp_monitoring_repo import CheckResultRepository
from app.services.endp_monitoring_service import MonitoringSerivce

# sites
from app.repository.sites_repo import SiteRepository
from app.services.sites_service import SiteService

# sites
from app.repository.endpoints_repo import EndpointRepository
from app.services.endpoints_service import EndpointService

from app.dependencies.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession


def get_monitoring_service(session: AsyncSession = Depends(get_db)):
    repo = CheckResultRepository(session)

    return MonitoringSerivce(repo)


def get_site_service(session: AsyncSession = Depends(get_db)):
    repo = SiteRepository(session)

    return SiteService(repo)


def get_endpoint_service(session: AsyncSession = Depends(get_db)):
    repo = EndpointRepository(session)

    return EndpointService(repo)