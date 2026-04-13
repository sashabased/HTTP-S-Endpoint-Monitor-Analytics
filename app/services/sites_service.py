import urllib.parse as ups

from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, EndpointCreate
from app.repository.interfaces import UnitOfWorkProtocol

class SiteService():
    def __init__(self, uow: UnitOfWorkProtocol):
        self.uow = uow


    async def create_url(self, user_input: SiteCreate):
        url_to_parse = user_input.base_url.strip().lower()

        if "://" not in url_to_parse:
                url_to_parse = f"https://{url_to_parse}"

        url_data = ups.urlparse(url_to_parse)
            
        if not url_data.netloc or "." not in url_data.netloc:
            raise ValidationError("URL domain is None")
            
        if url_data.scheme not in ('http', 'https'):
            raise ValidationError("URL scheme must be http/https")
            
        if url_data.path not in ('', '/'):
            raise ValidationError("URL path must be empty or '/'")

        user_input.base_url = url_to_parse.rstrip('/')
        
        async with self.uow:
            return await self.uow.sites.add_url(user_input)  
        

    async def get_urls(self):
        async with self.uow:
            return await self.uow.sites.select_urls()
    

    async def get_url(self, url_id: int):
        async with self.uow:
            return await self.uow.sites.select_url(url_id)
    

    async def update_url(self, url_id: int, user_input: SiteEdit):
        async with self.uow:
            return await self.uow.sites.edit_url(url_id, user_input)
    

    async def delete_url(self, url_id: int):
        async with self.uow:
            await self.uow.sites.drop_url(url_id)
    

    async def create_endpoint(self, url_id: int, user_input: EndpointCreate):
        user_input.path = "/" + user_input.path.strip("/")
        async with self.uow:
            return await self.uow.sites.add_endpoint(url_id, user_input)