import urllib.parse as ups

from app.core.exceptions import DatabaseError, NotFoundError, ValidationError
from app.schemas.endpoint_schema import SiteCreate, SiteEdit
from app.repository.sites_repo import SiteRepository

class SiteService():
    def __init__(self, repo: SiteRepository):
        self.repo = repo

    async def validate_user_url(self, user_input: SiteCreate):
        
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

        response = await self.repo.add_validated_url(user_input)  
            
        return response
        
    async def validate_all_urls(self):
    
        response = await self.repo.get_all_urls()

        return response
    
    async def validate_url(self, url_id: int):

        respone = await self.repo.get_one_url(url_id)

        if not respone:
            raise NotFoundError("URL not found")
        
        return respone  
    
    async def check_to_edit_url(self, url_id: int, user_input: SiteEdit):
       
        response = await self.repo.edit_url(url_id, user_input)

        if not response:
            raise NotFoundError("URL not found")
        
        return response
    
    async def check_to_del_url(self, url_id: int):

        response = await self.repo.delete_url(url_id)

        if not response:
            raise NotFoundError("URL not found")
            
        return {"status": "deleted"}