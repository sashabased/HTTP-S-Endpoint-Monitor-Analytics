from app import http_client

import urllib.parse as ups

from app.core.exceptions import EndpointIdError, DatabaseGetError, InvalidUrlPathError, DatabaseError, InvalidUrlSchemeError, InvalidUrlDomainError, DatabaseDeleteError
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate, SiteEdit, EndpointEdit
from app.repository.endpoint_repo import UrlRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UrlService():
    def __init__(self, session: AsyncSession):
        self.session = session

    # ТУТ ПО ЮРЛАМ!!!

    async def validate_user_url(self, user_input: SiteCreate):
        
            url_to_parse = user_input.base_url.strip().lower()

            if "://" not in url_to_parse:
                url_to_parse = f"https://{url_to_parse}"

            url_data = ups.urlparse(url_to_parse)
            
            if not url_data.netloc or "." not in url_data.netloc:
                raise InvalidUrlDomainError("URL domain is None")
            
            if url_data.scheme not in ('http', 'https'):
                raise InvalidUrlSchemeError("URL protocol must be http/https")
            
            if url_data.path not in ('', '/'):
                raise InvalidUrlPathError("URL path must be empty or '/'")

            user_input.base_url = url_to_parse.rstrip('/')

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
    
    async def check_to_edit_url(self, url_id: int, user_input: SiteEdit):
       
        response = await UrlRepository(self.session).edit_url(url_id, user_input)

        if not response or response is None:
            raise InvalidUrlPathError("URL with this id dont exist")
        
        try:
            await self.session.commit()
            await self.session.refresh(response)

            return response
        
        except Exception as e:
            await self.session.rollback()

            raise DatabaseError
    
    async def check_to_del_url(self, url_id: int):

        try:
            response = await UrlRepository(self.session).delete_url(url_id)

            if not response or response is None:
                return None
            
            await self.session.commit()
            return {"status": "deleted"}
        
        except Exception as e:
            await self.session.rollback()

            raise DatabaseDeleteError("Delete from db was unsuccsessfull, object dont exists")

    # ТУТ ПО ЭНДПОИНТАМ ЮРЛОВ!!!   

    async def validate_endp_to_post(self, url_id: int, user_input: EndpointCreate):
        
        edit_path = user_input.path
        edit_path = "/" + edit_path.strip("/")
        user_input.path = edit_path

        try:
            response = await UrlRepository(self.session).add_endp_to_url(url_id, user_input)

            if not response or response is None:
                raise InvalidUrlPathError("URL with this id dont exist")
            
            await self.session.commit()
            await self.session.refresh(response)

            return response
        
        except IntegrityError as e:
            await self.session.rollback()
            print(e)

            raise DatabaseError("URL already have this endpoint")
        
    async def check_to_patch_endp(self, endp_id: int, user_input: EndpointEdit):

        validated_path = user_input.path.strip('/')
        user_input.path = '/' + validated_path

        response = await UrlRepository(self.session).edit_endp(endp_id, user_input)

        if not response or response is None:
            raise InvalidUrlPathError("Endpoint with this id dont exist")
            
        try:  
            await self.session.commit()
            await self.session.refresh(response)

            return response
        
        except Exception as e:
            await self.session.rollback()

            raise DatabaseError()

    async def check_to_del_endp(self, endp_id: int):

        response = await UrlRepository(self.session).delete_endp(endp_id)

        if response is False:
            raise DatabaseDeleteError("Endpoint already deleted or dont exist")

        try:
            await self.session.commit()
            return {"status": "deleted"}

        except Exception as e:
            await self.session.rollback()

            raise DatabaseError()
        
    async def validate_endp_get(self, endp_id: int):

        response = await UrlRepository(self.session).get_endp(endp_id)

        if not response or response is None:
            raise EndpointIdError("Endpoint with this Id not found")
        
        return response
        
            

async def check_endpoint(url):
    response = await http_client.client.get(url)
    print(f"Page and endpoint status: {response.status_code}")