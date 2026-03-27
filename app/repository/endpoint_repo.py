from app import http_client

from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, SiteDelete

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UrlRepository():
    def __init__(self, session: AsyncSession):
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
    
    async def delete_url(self, user_input: SiteDelete):

        obj_to_del = await self.session.scalar(
            select(Site)
            .where(Site.id == user_input.id)
        )

        if obj_to_del:
            await self.session.delete(obj_to_del)
            return True
        
        return False