from app.repository.endp_monitoring_repo import CheckResultRepository
from app.repository.sites_repo import SiteRepository
from app.repository.endpoints_repo import EndpointRepository
from app.dependencies.db import DBSessionDep

from fastapi import Depends

from typing import Annotated

def get_check_result_repo(session: DBSessionDep) -> CheckResultRepository:
    return CheckResultRepository(session)
CheckResultRepoDep = Annotated[CheckResultRepository, Depends(get_check_result_repo)]

def get_site_repo(session: DBSessionDep) -> SiteRepository:
    return SiteRepository(session)
SiteRepoDep = Annotated[SiteRepository, Depends(get_site_repo)]

def get_endpoint_repo(session: DBSessionDep) -> EndpointRepository:
    return EndpointRepository(session)
EndpointRepoDep = Annotated[EndpointRepository, Depends(get_endpoint_repo)]