from app import http_client

from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UrlRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    # ТУТ ПО ЮРЛАМ!!!

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
    
    async def get_one_url(self, url_id: int):

        response = await self.session.scalar(
            select(Site)
            .where(Site.id == url_id)
        )
        
        return response
    
    async def delete_url(self, url_id: int):

        obj_to_del = await self.session.scalar(
            select(Site)
            .where(Site.id == url_id)
        )

        if obj_to_del:
            await self.session.delete(obj_to_del)
            return True
        
        return False
    
    # ТУТ ПО ЭНДПОИНТАМ ЮРЛОВ!!!

    async def add_endp_to_url(self, url_id: int, user_input: EndpointCreate):

        url_check = await self.session.scalar(select(Site).where(Site.id == url_id))

        if url_check:

            new_endp = Endpoint(
                path = user_input.path,
                sampling_interval = user_input.sampling_interval,
                is_active = user_input.is_active,
                site_id = url_id
            )

            self.session.add(new_endp)

            return new_endp
        
        return None