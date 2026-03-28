from app import http_client

import urllib.parse as ups

from app.core.exceptions import DatabaseGetError, InvalidUrlPathError, DatabaseError, InvalidUrlSchemeError, InvalidUrlDomainError, DatabaseDeleteError
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate
from app.repository.endpoint_repo import UrlRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UrlService():
    def __init__(self, session: AsyncSession):
        self.session = session

    # ТУТ ПО ЮРЛАМ!!!

    async def validate_user_url(self, user_input: SiteCreate):
        
            url_to_parse = user_input.url.strip().lower()

            if "://" not in url_to_parse:
                url_to_parse = f"https://{url_to_parse}"

            url_data = ups.urlparse(url_to_parse)
            
            if not url_data.netloc or "." not in url_data.netloc:
                raise InvalidUrlDomainError("URL domain is None")
            
            if url_data.scheme not in ('http', 'https'):
                raise InvalidUrlSchemeError("URL protocol must be http/https")
            
            if url_data.path not in ('', '/'):
                raise InvalidUrlPathError("URL path must be empty or '/'")

            user_input.url = url_to_parse.rstrip('/')

            try:
                response = await UrlRepository(self.session).add_validated_url(user_input)
                await self.session.commit()
                await self.session.refresh(response)

                return response
            
            except Exception as e:
                await self.session.rollback()

                print(e)
                raise DatabaseError("Failed to save validated URL") from e
        
    async def validate_all_urls(self):
    
        response = await UrlRepository(self.session).get_all_urls()
        return response
    
    async def validate_url(self, url_id: int):

        respone = await UrlRepository(self.session).get_one_url(url_id)

        if not respone or respone is None:
            raise DatabaseGetError("URL with this id dont exists, use another one")
        
        return respone  
    
    async def check_to_del_url(self, url_id: int):

        try:
            response = await UrlRepository(self.session).delete_url(url_id)

            if not response:
                return None
            
            await self.session.commit()
            return {"status": "deleted"}
        
        except Exception as e:
            await self.session.rollback()

            raise DatabaseDeleteError("Delete from db was unsuccsessfull, object dont exists")

    # ТУТ ПО ЭНДПОИНТАМ ЮРЛОВ!!!   

    async def validate_endp_to_post(self, url_id: int, user_input: EndpointCreate):
        try:
            response = await UrlRepository(self.session).add_endp_to_url(url_id, user_input)

            if not response or response is None:
                raise InvalidUrlPathError("URL with this id dont exist")
            
            await self.session.commit()
            await self.session.refresh(response)

            return response
        
        except IntegrityError:
            await self.session.rollback()

            raise DatabaseError("URL already have this endpoint")

async def check_endpoint(url):
    response = await http_client.client.get(url)
    print(f"Page and endpoint status: {response.status_code}")