from app import http_client

import httpx as hx

import urllib.parse as ups

from app.core.exceptions import EndpointIdError, DatabaseGetError, InvalidUrlPathError, DatabaseError, InvalidUrlSchemeError, InvalidUrlDomainError, DatabaseDeleteError
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate, SiteEdit, EndpointEdit
from app.repository.endp_monitoring_repo import CheckResultRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class MonitoringSerivce():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _do_ping(self, url: str, method: str, timeout: float):
        
        try:
            
            response = await http_client.client.request(
                method=method,
                url=url,
                timeout=timeout,
                follow_redirects=True
            )

            return {
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "is_available": 200 <= response.status_code < 400,
                "error_details": None
            }
        
        except hx.RequestError as exc:
            return {
                "status_code": 0,
                "response_time": 0.0,
                "is_available": False,
                "error_details": f"Network error: {str(exc)}"
            }
        
        except Exception as e:
            return {
                "status_code": 0,
                "response_time": 0.0,
                "is_available": False,
                "error_details": f"Unknown error: {str(e)}"
            }

    async def check_to_ping_endps(self):
        
        sites = await (CheckResultRepository(self.session)
                            .get_active_endpoints_with_sites()
        )

        if sites is None or not sites:
            raise DatabaseGetError("URL have no active endpoints")
        
        all_results = []

        for site in sites:
            for endp in site.endpoints:
                
                full_url = f"{site.base_url}{endp.path}"

                ping_result = await self._do_ping(full_url, endp.method, endp.timeout)

                result_model = CheckResult(
                    **ping_result,
                    endpoint_id=endp.id
                )

                all_results.append(result_model)

        response = await CheckResultRepository(self.session).bulk_save(all_results)

        try:
            await self.session.commit()
            await self.session.refresh(response)

            return response

        except Exception as e:
            await self.session.rollback()

            print(e)