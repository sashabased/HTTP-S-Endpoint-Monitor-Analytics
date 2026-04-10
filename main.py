from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import uvicorn

from app import http_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import httpx
import asyncio
import sys
import logging

from app.core.handlers import register_exception_handler
from app.routers.endpoints_router import endpoints
from app.routers.sites_router import sites
from app.routers.endp_monitoring_router import endp_monitor
from app.core.logging import setup_logging

from contextlib import asynccontextmanager

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    http_client.client = httpx.AsyncClient()

    yield

    await http_client.client.aclose()
    logger.info("Application shutting down...")

app = FastAPI(title='Dashboard HTTP tools', lifespan=lifespan)

register_exception_handler(app)

@app.get("/")
async def get_loop_type():
    return {"loop_type": str(asyncio.get_event_loop_policy())}

app.include_router(endpoints)
app.include_router(sites)
app.include_router(endp_monitor)

if __name__ == "__main__":

    uvicorn.run(
        "main.app", 
        host="127.0.0.1", 
        port=8000, 
        loop='asyncio',
        reload=True
    )
