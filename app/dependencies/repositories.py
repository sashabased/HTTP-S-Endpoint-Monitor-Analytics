from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.endp_monitoring_repo import CheckResultRepository
from app.repository.sites_repo import SiteRepository
from app.repository.endpoints_repo import EndpointRepository
from app.dependencies.db import get_db


def get_check_result_repo(session: AsyncSession = Depends(get_db)) -> CheckResultRepository:
    return CheckResultRepository(session)


def get_site_repo(session: AsyncSession = Depends(get_db)) -> SiteRepository:
    return SiteRepository(session)


def get_endpoint_repo(session: AsyncSession = Depends(get_db)) -> EndpointRepository:
    return EndpointRepository(session)