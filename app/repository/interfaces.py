from typing import Protocol, List

from app.models.endpointer_models import CheckResult, Site, Endpoint
from app.schemas.endpoint_schema import EndpointEdit, EndpointCreate, SiteCreate, SiteEdit
from app.UnitOfWork.uow import UnitOfWork


class CheckResultRepositoryProtocol(Protocol):
    async def bulk_save(self, data: List[CheckResult]) -> None:
        ...
    async def get_active_endpoints(self) -> List[Endpoint]:
        ...


class EndpointsRepositoryProtocol(Protocol):
    async def edit_endp(self, endp_id: int, user_input: EndpointEdit) -> Endpoint:
        ...
    async def drop_endp(self, endp_id: int) -> None:
        ...
    async def select_endp(self, endp_id: int) -> Endpoint:
        ...


class SiteRepositoryProtocol(Protocol):
    async def add_url(self, user_input: SiteCreate) -> Site:
        ...
    async def select_urls(self) -> List[Site]:
        ...
    async def select_url(self, url_id: int) -> Site:
        ...
    async def edit_url(self, url_id: int, user_input: SiteEdit) -> Site:
        ...
    async def drop_url(self, url_id: int) -> None:
        ...
    async def add_endpoint(self, url_id: int, user_input: EndpointCreate) -> Endpoint:
        ...


class UnitOfWorkProtocol(Protocol):
    sites: SiteRepositoryProtocol
    endpoints: EndpointsRepositoryProtocol
    check_results: CheckResultRepositoryProtocol

    async def __aenter__(self) -> "UnitOfWorkProtocol": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...