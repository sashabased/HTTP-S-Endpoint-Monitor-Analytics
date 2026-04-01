from app import http_client

from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate, SiteEdit, EndpointEdit

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

class CheckResultRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_endpoints_with_sites(self, url_id: int):

        active_endps = await self.session.scalars(
            select(Endpoint)
            .where(Endpoint.site_id == url_id)
            .where(Endpoint.is_active == True)
        )

        return active_endps.unique().all()