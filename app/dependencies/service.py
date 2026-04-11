from fastapi import Depends

import httpx as hx
from app.dependencies.http import get_http_client

from app.services.endp_monitoring_service import MonitoringSerivce
from app.services.sites_service import SiteService
from app.services.endpoints_service import EndpointService

from app.repository.endp_monitoring_repo import CheckResultRepository
from app.repository.sites_repo import SiteRepository
from app.repository.endpoints_repo import EndpointRepository

from app.dependencies.repositories import (
    get_check_result_repo,
    get_site_repo,
    get_endpoint_repo,
)


def get_monitoring_service(
        repo: CheckResultRepository = Depends(get_check_result_repo),
        client: hx.AsyncClient = Depends(get_http_client)
) -> MonitoringSerivce:
    return MonitoringSerivce(repo, client)


def get_site_service(
        repo: SiteRepository = Depends(get_site_repo)
) -> SiteService:
    return SiteService(repo)


def get_endpoint_service(
        repo: EndpointRepository = Depends(get_endpoint_repo)
) -> EndpointRepository:
    return SiteService(repo)