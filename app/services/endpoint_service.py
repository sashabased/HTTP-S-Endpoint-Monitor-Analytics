from app import http_client

import urllib.parse as ups

from app.core.exceptions import InvalidUrlPathError, DatabaseError, InvalidUrlSchemeError, InvalidUrlDomainError, DatabaseDeleteError
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, SiteDelete
from app.repository.endpoint_repo import UrlRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UrlService():
    def __init__(self, session: AsyncSession):
        self.session = session

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
    
    async def check_to_del_url(self, user_input: SiteDelete):

        try:
            response = await UrlRepository(self.session).delete_url(user_input)

            if not response:
                return None
            
            await self.session.commit()
            return {"status": "deleted"}
        
        except Exception as e:
            await self.session.rollback()

            raise DatabaseDeleteError("Delete from db was unsuccsessfull, object dont exists")
        
        
    # @staticmethod
    # async def get_url_by_id(site_id: int, session: AsyncSession):
    #     try:
    #         response = await session.get(Site, site_id)
    #         return response
        
    #     except Exception as e:
    #         print(f'Error raised at func: get_url_by_id -> {str(e)}')

    #         return None
        
    # @staticmethod
    # async def get_all_urls(sesion: AsyncSession):
    #     try:
    #         response = await sesion.scalars(select(Site))
    #         if not response:
    #             return None
    #         return response.all()
        
    #     except Exception as e:
    #         print(f'Error raised at func: get_all_urls -> {str(e)}')

    #         return None
    
    # # ТУТ НАЧИНАЮТСЯ ЕНДПОИНТЫ ЧТО БЫ НЕ ТЕРЯТЬСЯ В КОДЕ С ЮРЛАМИ ВСЕ ВЫШЕ !!!

    # @staticmethod
    # async def add_endpoint_to_url(site_id: int, user_input: EndpointCreate, session: AsyncSession):
    #     try:
    #         site = await session.get(Site, site_id)
    #         if site is None:
    #             return None
    #         if user_input.path is None:
    #             return None
    #         val_endp = (user_input.path).strip('/')
    #         val_endp = ('/' + val_endp)
    #         new_endpoint = Endpoint(
    #             path = val_endp,
    #             sampling_interval = user_input.sampling_interval,
    #             is_active = user_input.is_active,
    #             site_id = site.id
    #         )
    #         session.add(new_endpoint)

    #         await session.commit()
    #         await session.refresh(new_endpoint)

    #         return new_endpoint
    #     except Exception as e:
    #         print(f'Error raised at func: add_endpoint_to_url -> {str(e)}')
    #         await session.rollback()

    #         return None
        
    # @staticmethod
    # async def get_all_site_endpoints(site_id: str, session: AsyncSession):
    #     try:
    #         site = await session.get(Site, site_id)
    #         if site is None or not site:
    #             return None
            
    #         endpoints = await session.scalars(
    #             select(Endpoint)
    #             .where(Endpoint.site_id == site.id)
    #         )
    #         if endpoints is None or not endpoints:
    #             return None

    #         return site.base_url, endpoints.all()
        
    #     except Exception as e:
    #         print(f'Error raised at func: get_all_site_endpoints -> {str(e)}')

    #         return None

async def check_endpoint(url):
    response = await http_client.client.get(url)
    print(f"Page and endpoint status: {response.status_code}")