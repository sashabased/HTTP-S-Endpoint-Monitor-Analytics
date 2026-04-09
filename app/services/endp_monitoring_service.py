from app import http_client

import asyncio
import httpx as hx

from app.core.exceptions import NotFoundError, AlreadyExistsError, DatabaseError, ValidationError
from app.models.endpointer_models import CheckResult
from app.repository.endp_monitoring_repo import CheckResultRepository

class MonitoringSerivce():
    def __init__(self, repo: CheckResultRepository):
        self.repo = repo

    
    async def _ping_and_format(self, endp):

        full_url = f"{endp.site.base_url.rstrip('/')}/{endp.path.lstrip('/')}"

        ping_data = await self._do_ping(full_url, endp.method, endp.timeout)

        return CheckResult(**ping_data, endpoint_id=endp.id)


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
        
        endpoints = await self.repo.get_active_endpoints()
        
        if not endpoints:
            return []

        tasks = []

        for endp in endpoints:

            tasks.append(self._ping_and_format(endp))
        
        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = [r for r in all_results if isinstance(r, CheckResult)]

        if valid_results:
            await self.repo.bulk_save(valid_results)

        return all_results