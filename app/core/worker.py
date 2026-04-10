from dotenv import load_dotenv
load_dotenv()

import logging
import httpx

from arq import cron
from arq.connections import RedisSettings

from app import http_client
from app.database.session import session_maker
from app.repository.endp_monitoring_repo import CheckResultRepository
from app.services.endp_monitoring_service import MonitoringSerivce

logger = logging.getLogger(__name__)


async def run_monitoring_task(ctx):
    async with session_maker() as session:
        repo = CheckResultRepository(session)
        service = MonitoringSerivce(repo)

        logger.info("ARQ: Monitoring cycle started")

        try:
            await service.check_to_ping_endps()
            logger.info("ARQ: Monitoring cycle finished")
        except Exception:
            logger.exception("ARQ: Critical error in monitoring task")


async def startup(ctx):
    http_client.client = httpx.AsyncClient()
    logger.info("ARQ: Worker started")

async def shutdown(ctx):
    await http_client.client.aclose()
    logger.info("ARQ: Worker stopped")

class WorkerSettings:
    functions = [run_monitoring_task]

    cron_jobs = [
        cron(run_monitoring_task, minute=None, second=0)
    ]

    redis_settings = RedisSettings(host='127.0.0.1', port=6379)
    on_startup = startup
    on_shutdown = shutdown