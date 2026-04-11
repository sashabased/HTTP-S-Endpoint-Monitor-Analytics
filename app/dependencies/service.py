from fastapi import Depends

from app.dependencies.http import ClientSessionDep
from app.services.endp_monitoring_service import MonitoringSerivce
from app.services.sites_service import SiteService
from app.services.endpoints_service import EndpointService

from app.dependencies.repositories import SiteRepoDep, EndpointRepoDep, CheckResultRepoDep
from typing import Annotated

def get_monitoring_service(
        repo: CheckResultRepoDep, 
        client: ClientSessionDep
) -> MonitoringSerivce:
    return MonitoringSerivce(repo, client)
CheckResltServiceDep = Annotated[MonitoringSerivce, Depends(get_monitoring_service)]

def get_site_service(repo: SiteRepoDep) -> SiteService:
    return SiteService(repo)
SiteServiceDep = Annotated[SiteService, Depends(get_site_service)]


def get_endpoint_service(repo: EndpointRepoDep) -> EndpointService:
    return EndpointService(repo)
EndpointServiceDep = Annotated[EndpointService, Depends(get_endpoint_service)]