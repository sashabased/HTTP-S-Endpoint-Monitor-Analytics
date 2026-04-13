from app.models.endpointer_models import Endpoint
from app.schemas.endpoint_schema import EndpointEdit
from app.core.exceptions import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession



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

        self.session.add(obj_to_edit)
        return obj_to_edit
    

    async def drop_endp(self, endp_id: int):
        obj_to_del = await self.session.get(Endpoint, endp_id)

        if not obj_to_del:
            raise NotFoundError("Endpoind not found")
        
        self.session.delete(obj_to_del)
    
    
    async def select_endp(self, endp_id: int):
        obj = await self.session.get(Endpoint, endp_id)

        if not obj:
            raise NotFoundError("Endpoint not found")

        return obj