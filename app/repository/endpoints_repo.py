from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import EndpointEdit
from app.core.exceptions import NotFoundError, AlreadyExistsError, DatabaseError

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class EndpointRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def edit_endp(self, endp_id: int, user_input: EndpointEdit):

        obj_to_edit = await self.session.get(Endpoint, endp_id)

        if not obj_to_edit:
            raise NotFoundError("Endpoind not found")
            
        data_to_put = user_input.model_dump(exclude_unset=True)

        for key, value in data_to_put.items():
            setattr(obj_to_edit, key, value)

        try:
            self.session.add(obj_to_edit)

            await self.session.commit()
            await self.session.refresh(obj_to_edit)

            return obj_to_edit
        
        except IntegrityError:
            await self.session.rollback()

            raise AlreadyExistsError("Endpoint already exists")
        
        except Exception:
            await self.session.rollback()

            raise DatabaseError("Failed to edit endpoint")
    

    async def drop_endp(self, endp_id: int):

        obj_to_del = await self.session.scalar(
            select(Endpoint)
            .where(Endpoint.id == endp_id)
        )

        if not obj_to_del:
            raise NotFoundError("Endpoind not found")
        
        await self.session.delete(obj_to_del)

        try:
            await self.session.commit()
            
        except Exception:
            await self.session.rollback()

            raise DatabaseError("Failed to delete endpoint")
    
    
    async def select_endp(self, endp_id: int):

        obj = await self.session.scalar(
            select(Endpoint)
            .where(Endpoint.id == endp_id)
        )

        if not obj:
            raise NotFoundError("Endpoint not found")

        return obj