from app.core.exceptions import NotFoundError 
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import EndpointEdit
from app.repository.endpoints_repo import EndpointRepository


class EndpointService():
    def __init__(self, repo: EndpointRepository):
        self.repo = repo

        
    async def check_to_patch_endp(self, endp_id: int, user_input: EndpointEdit):

        validated_path = user_input.path.strip('/')
        user_input.path = '/' + validated_path

        response = await self.repo.edit_endp(endp_id, user_input)

        if not response or response is None:
            raise NotFoundError("Endpoint not found")
        
        return response


    async def check_to_del_endp(self, endp_id: int):

        response = await self.repo.delete_endp(endp_id)

        if response is False:
            raise NotFoundError("Endpoint not found")
        
        return {"status": "deleted"}
      
        
    async def validate_endp_get(self, endp_id: int):

        response = await self.repo.get_endp(endp_id)

        if not response or response is None:
            raise NotFoundError("Endpoint not found")
        
        return response