from app import http_client

import httpx as hx

from app.core.exceptions import NotFoundError, AlreadyExistsError, DatabaseError, ValidationError
from app.models.endpointer_models import CheckResult
from app.repository.endp_monitoring_repo import CheckResultRepository

class MonitoringSerivce():
    def __init__(self, repo: CheckResultRepository):
        self.repo = repo

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
        
        sites = await self.repo.get_active_endpoints_with_sites()
        
        if not sites:
            print(f"No active endpoints found")
            return []

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
        
        await self.repo.bulk_save(all_results)

        return all_results