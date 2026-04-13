import asyncio
import httpx as hx

from app.models.endpointer_models import CheckResult
from app.repository.interfaces import UnitOfWorkProtocol

import logging

logger = logging.getLogger(__name__)


class MonitoringSerivce():
    def __init__(self, uow: UnitOfWorkProtocol, client: hx.AsyncClient):
        self.uow = uow
        self.client = client

    
    async def _ping_and_format(self, endp):
        full_url = f"{endp.site.base_url.rstrip('/')}/{endp.path.lstrip('/')}"
        ping_data = await self._do_ping(full_url, endp.method, endp.timeout)

        return CheckResult(**ping_data, endpoint_id=endp.id)


    async def _do_ping(self, url: str, method: str, timeout: float):
        try:
            response = await self.client.request(
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
            logger.warning(f"Network error while pinging {url}: {exc}")

            return {
                "status_code": 0,
                "response_time": 0.0,
                "is_available": False,
                "error_details": f"Network error: {str(exc)}"
            }
        except Exception as e:
            logger.exception(f"Unexpected error during pinging {url}")

            return {
                "status_code": 0,
                "response_time": 0.0,
                "is_available": False,
                "error_details": f"Unknown error: {str(e)}"
            }


    async def check_to_ping_endps(self):
        async with self.uow:
            endpoints = await self.uow.check_results.get_active_endpoints()

        if not endpoints:
            logger.info("No active endpoints to check")
            return []

        logger.info(f"Starting check for {len(endpoints)} endpoints")
        tasks = []

        for endp in endpoints:

            tasks.append(self._ping_and_format(endp))

        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        errors_count = sum(1 for r in all_results if isinstance(r, Exception))

        if errors_count > 0:
            logger.error(f"Task gathering finished with {errors_count} critical errors")
        valid_results = [r for r in all_results if isinstance(r, CheckResult)]

        if valid_results:
            try:
                async with self.uow:
                    await self.uow.check_results.bulk_save(valid_results)

                logger.info(f"Succsessfully saved {len(valid_results)} ping results")
            except Exception as e:
                logger.error(f"Failed to save results: {e}")
            
        return valid_results