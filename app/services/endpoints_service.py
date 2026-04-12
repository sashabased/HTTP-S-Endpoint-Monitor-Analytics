from app.core.exceptions import NotFoundError 
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import EndpointEdit
from app.repository.interfaces import EndpointsRepositoryProtocol


class EndpointService():
    def __init__(self, repo: EndpointsRepositoryProtocol):
        self.repo = repo

        
    async def update_endp(self, endp_id: int, user_input: EndpointEdit):

        validated_path = user_input.path.strip('/')
        user_input.path = '/' + validated_path

        return await self.repo.edit_endp(endp_id, user_input)


    async def delete_endp(self, endp_id: int):

        await self.repo.drop_endp(endp_id)

        
    async def get_endpoint(self, endp_id: int):

        return await self.repo.select_endp(endp_id)