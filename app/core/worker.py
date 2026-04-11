from dotenv import load_dotenv
load_dotenv()

import os

import logging
import httpx as hx

from arq import cron
from arq.connections import RedisSettings

from app.dependencies.http import get_http_client
from app.database.session import db_manager
from app.repository.endp_monitoring_repo import CheckResultRepository
from app.services.endp_monitoring_service import MonitoringSerivce

logger = logging.getLogger(__name__)


async def run_monitoring_task(ctx):
    client: hx.AsyncClient = ctx['client']
    session_maker = db_manager.get_session_maker()

    if not client:
        logger.exception("ARQ: cannot get httpx client for worker")

    async with session_maker() as session:
        repo = CheckResultRepository(session)
        service = MonitoringSerivce(repo, client)

        logger.info("ARQ: Monitoring cycle started")

        try:
            await service.check_to_ping_endps()
            logger.info("ARQ: Monitoring cycle finished")
        except Exception:
            logger.exception("ARQ: Critical error in monitoring task")


async def startup(ctx):
    ctx['client'] = hx.AsyncClient()
    db_manager.init(os.getenv("DATABASE_URL"))

    logger.info("ARQ: Worker started")


async def shutdown(ctx):
    client: hx.AsyncClient = ctx.get('client')

    await db_manager.close()

    if client:
        await client.aclose()
    logger.info("ARQ: Worker stopped")


class WorkerSettings:
    functions = [run_monitoring_task]

    cron_jobs = [
        cron(run_monitoring_task, minute=None, second=0)
    ]

    redis_settings = RedisSettings(host='127.0.0.1', port=6379)
    on_startup = startup
    on_shutdown = shutdown