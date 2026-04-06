from sqlalchemy.exc import IntegrityError

from app.models.endpointer_models import Site, Endpoint
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate, SiteEdit
from app.core.exceptions import AlreadyExistsError

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SiteRepository():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_validated_url(self, user_input: SiteCreate):

        new_url = Site(
            base_url=user_input.base_url,
            name=user_input.name
        )

        self.session.add(new_url)

        try:
            await self.session.commit()
            await self.session.refresh(new_url)

            return new_url
        
        except Exception:
            await self.session.rollback()

            raise
    

    async def get_all_urls(self) -> List[Site]:

        objs = await self.session.scalars(select(Site))

        return objs.all()
    

    async def get_one_url(self, url_id: int):

        obj = await self.session.scalar(
            select(Site)
            .where(Site.id == url_id)
            .options(joinedload(Site.endpoints))
        )
        
        return obj
    

    async def edit_url(self, url_id: int, user_input: SiteEdit):
        
        obj_to_upd = await self.session.get(Site, url_id)

        if obj_to_upd:

            data_to_put = user_input.model_dump(exclude_unset=True)

            for key, item in data_to_put.items():
                setattr(obj_to_upd, key, item)

            self.session.add(obj_to_upd)

            try:
                await self.session.commit()
                await self.session.refresh(obj_to_upd)

                return obj_to_upd

            except Exception:
                await self.session.rollback()

                raise
        
        return None


    async def delete_url(self, url_id: int):

        obj_to_del = await self.session.scalar(
            select(Site)
            .where(Site.id == url_id)
        )

        if obj_to_del:
            await self.session.delete(obj_to_del)
            
            try:
                await self.session.commit()

                return True
            
            except Exception:
                await self.session.rollback()

                raise
        
        return False
    

    async def add_endp_to_url(self, url_id: int, user_input: EndpointCreate):

        url_check = await self.session.get(Site, url_id)

        if url_check:

            new_endp = Endpoint(
                path = user_input.path,
                sampling_interval = user_input.sampling_interval,
                is_active = user_input.is_active,
                method = user_input.method,
                timeout = user_input.timeout,
                site_id = url_id
            )

            self.session.add(new_endp)

            try:
                await self.session.commit()
                await self.session.refresh(new_endp)

                return new_endp
            
            except IntegrityError:
                await self.session.rollback()

                raise AlreadyExistsError

            except Exception:
                await self.session.rollback()

                raise
        
        return None