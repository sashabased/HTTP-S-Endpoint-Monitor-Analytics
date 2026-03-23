from app import http_client

import urllib.parse as ups

from fastapi import Depends
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, SiteRead

from sqlalchemy.ext.asyncio import AsyncSession

class EndpointService():

    @staticmethod
    async def post_user_url(user_input: SiteCreate, session: AsyncSession):
        try:
            url_data = ups.urlparse(user_input.url)
            if url_data.path in ('', '/'):
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

async def check_endpoint(url):
    response = await http_client.client.get(url)
    print(f"Page and endpoint status: {response.status_code}")