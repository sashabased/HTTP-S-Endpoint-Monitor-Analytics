from app import http_client

import urllib.parse as ups

from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, SiteRead, EndpointRead, EndpointCreate, EndpointEdit

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class EndpointService():

    @staticmethod
    async def post_user_url(user_input: SiteCreate, session: AsyncSession):
        try:
            url_data = ups.urlparse(user_input.url)
            if url_data.path in ('', '/'):
                # обрежу слеш юрла потомушто потом ендпоинт с слешем прилетит распаршенный
                user_input.url = user_input.url.strip('/')
                new_url = Site(
                    base_url=user_input.url,
                    name=user_input.name
                )

                session.add(new_url)
                await session.commit()
                await session.refresh(new_url)

                return new_url
            else:
                return 'url/endp'
        
        except Exception as e:
            await session.rollback()
            print(f'Error raised at func: post_user_url -> {str(e)}')

            return None
        
    @staticmethod
    async def get_url_by_id(site_id: int, session: AsyncSession):
        try:
            response = await session.get(Site, site_id)
            return response
        
        except Exception as e:
            print(f'Error raised at func: get_url_by_id -> {str(e)}')

            return None
        
    @staticmethod
    async def get_all_urls(sesion: AsyncSession):
        try:
            response = await sesion.scalars(select(Site))
            if not response:
                return None
            return response.all()
        
        except Exception as e:
            print(f'Error raised at func: get_all_urls -> {str(e)}')

            return None
    
    # ТУТ НАЧИНАЮТСЯ ЕНДПОИНТЫ ЧТО БЫ НЕ ТЕРЯТЬСЯ В КОДЕ С ЮРЛАМИ ВСЕ ВЫШЕ !!!

    @staticmethod
    async def add_endpoint_to_url(site_id: int, user_input: EndpointCreate, session: AsyncSession):
        try:
            site = await session.get(Site, site_id)
            if site is None:
                return None
            if user_input.path is None:
                return None
            val_endp = (user_input.path).strip('/')
            val_endp = ('/' + val_endp)
            new_endpoint = Endpoint(
                path = val_endp,
                sampling_interval = user_input.sampling_interval,
                is_active = user_input.is_active,
                site_id = site.id
            )
            session.add(new_endpoint)

            await session.commit()
            await session.refresh(new_endpoint)

            return new_endpoint
        except Exception as e:
            print(f'Error raised at func: add_endpoint_to_url -> {str(e)}')
            await session.rollback()

            return None
        
    @staticmethod
    async def get_all_site_endpoints(site_id: str, session: AsyncSession):
        try:
            site = await session.get(Site, site_id)
            if site is None or not site:
                return None
            
            endpoints = await session.scalars(
                select(Endpoint)
                .where(Endpoint.site_id == site.id)
            )
            if endpoints is None or not endpoints:
                return None

            return site.base_url, endpoints.all()
        
        except Exception as e:
            print(f'Error raised at func: get_all_site_endpoints -> {str(e)}')

            return None

async def check_endpoint(url):
    response = await http_client.client.get(url)
    print(f"Page and endpoint status: {response.status_code}")