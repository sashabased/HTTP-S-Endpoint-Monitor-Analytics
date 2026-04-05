from app.core.exceptions import NotFoundError 
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import EndpointEdit
from app.repository.endpoints_repo import EndpointRepository


class EndpointService():
    def __init__(self, repo: EndpointRepository):
        self.repo = repo

    # ПЕРЕНЕСТИ В СЕРВИС САЙТОВ  

    # async def validate_endp_to_post(self, url_id: int, user_input: EndpointCreate):
        
    #     edit_path = user_input.path
    #     edit_path = "/" + edit_path.strip("/")
    #     user_input.path = edit_path

    #     try:
    #         response = await UrlRepository(self.session).add_endp_to_url(url_id, user_input)

    #         if not response or response is None:
    #             raise InvalidUrlPathError("URL with this id dont exist")
            
    #         await self.session.commit()
    #         await self.session.refresh(response)

    #         return response
        
    #     except IntegrityError as e:
    #         await self.session.rollback()
    #         print(e)

    #         raise DatabaseError("URL already have this endpoint")
        
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