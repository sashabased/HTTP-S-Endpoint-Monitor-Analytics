from app.core.exceptions import DatabaseError 
from app.schemas.endpoint_schema import EndpointEdit
from app.repository.interfaces import UnitOfWorkProtocol

from sqlalchemy.exc import SQLAlchemyError


class EndpointService():
    def __init__(self, uow: UnitOfWorkProtocol):
        self.uow = uow

        
    async def update_endp(self, endp_id: int, user_input: EndpointEdit):
        validated_path = user_input.path.strip('/')
        user_input.path = '/' + validated_path

        try:
            async with self.uow:
                return await self.uow.endpoints.edit_endp(endp_id, user_input)
        except SQLAlchemyError as e:
            raise DatabaseError("Database error was raised") from e


    async def delete_endp(self, endp_id: int):
        async with self.uow:
            await self.uow.endpoints.drop_endp(endp_id)

        
    async def get_endpoint(self, endp_id: int):
        async with self.uow:
            return await self.uow.endpoints.select_endp(endp_id)