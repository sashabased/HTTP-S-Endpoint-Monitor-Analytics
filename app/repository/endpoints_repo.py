from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import EndpointEdit

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class EndpointRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    # ПЕРЕНЕСТИ В РЕПО САЙТА 

    # async def add_endp_to_url(self, url_id: int, user_input: EndpointCreate):

    #     url_check = await self.session.scalar(select(Site).where(Site.id == url_id))

    #     if url_check:

    #         new_endp = Endpoint(
    #             path = user_input.path,
    #             sampling_interval = user_input.sampling_interval,
    #             is_active = user_input.is_active,
    #             method = user_input.method,
    #             timeout = user_input.timeout,
    #             site_id = url_id
    #         )

    #         self.session.add(new_endp)

    #         return new_endp
        
    #     return None
    
    async def edit_endp(self, endp_id: int, user_input: EndpointEdit):

        obj_to_edit = await self.session.get(Endpoint, endp_id)

        if obj_to_edit:
            data_to_put = user_input.model_dump(exclude_unset=True)

            for key, value in data_to_put.items():
                setattr(obj_to_edit, key, value)

            self.session.add(obj_to_edit)

            await self.session.commit()
            await self.session.refresh(obj_to_edit)

            return obj_to_edit
        
        return None
    
    async def delete_endp(self, endp_id: int):

        obj_to_del = await self.session.scalar(
            select(Endpoint)
            .where(Endpoint.id == endp_id)
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
    
    async def get_endp(self, endp_id: int):

        obj = await self.session.scalar(
            select(Endpoint)
            .where(Endpoint.id == endp_id)
        )

        return obj