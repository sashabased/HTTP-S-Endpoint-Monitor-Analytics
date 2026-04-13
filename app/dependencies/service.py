from fastapi import Depends

from app.dependencies.http import ClientSessionDep
from app.services.endp_monitoring_service import MonitoringSerivce
from app.services.sites_service import SiteService
from app.services.endpoints_service import EndpointService
from app.UnitOfWork.uow import UnitOfWork

from typing import Annotated

def get_uow() -> UnitOfWork:
    return UnitOfWork()
UOWDep = Annotated[UnitOfWork, Depends(get_uow)]


def get_monitoring_service(
        uow: UOWDep, 
        client: ClientSessionDep
) -> MonitoringSerivce:
    return MonitoringSerivce(uow, client)
CheckResltServiceDep = Annotated[MonitoringSerivce, Depends(get_monitoring_service)]


def get_site_service(uow: UOWDep) -> SiteService:
    return SiteService(uow)
SiteServiceDep = Annotated[SiteService, Depends(get_site_service)]


def get_endpoint_service(uow: UOWDep) -> EndpointService:
    return EndpointService(uow)
EndpointServiceDep = Annotated[EndpointService, Depends(get_endpoint_service)]