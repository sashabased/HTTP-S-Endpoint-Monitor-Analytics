from app import http_client

from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, SiteRead, EndpointRead, EndpointCreate, EndpointEdit

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UrlRepository():
    def __init__(self, session):
        self.session = session

    async def add_validated_url(self, user_input: SiteCreate):
        new_url = Site(
            base_url=user_input.url,
            name=user_input.name
        )

        self.session.add(new_url)

        return new_url
    
    async def get_all_urls(self) -> List[Site]:
        response = await self.session.scalars(select(Site))

        return response.all()