import urllib.parse as ups

from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, EndpointCreate
from app.repository.interfaces import SiteRepositoryProtocol

class SiteService():
    def __init__(self, repo: SiteRepositoryProtocol):
        self.repo = repo


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

        response = await self.repo.add_url(user_input)  
            
        return response
        

    async def get_urls(self):
    
        response = await self.repo.select_urls()

        return response
    

    async def get_url(self, url_id: int):

        response = await self.repo.select_url(url_id)

        return response  
    

    async def update_url(self, url_id: int, user_input: SiteEdit):
       
        response = await self.repo.edit_url(url_id, user_input)

        return response
    

    async def delete_url(self, url_id: int):

        await self.repo.drop_url(url_id)
    

    async def create_endpoint(self, url_id: int, user_input: EndpointCreate):
        
        user_input.path = "/" + user_input.path.strip("/")

        response = await self.repo.add_endpoint(url_id, user_input)

        return response