from fastapi import FastAPI
import uvicorn

from app import http_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import httpx
import asyncio
import sys

from app.routers.endpoints_router import endpoints
from app.routers.sites_router import sites
from app.routers.endp_monitoring_router import endp_monitor

from contextlib import asynccontextmanager

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client.client = httpx.AsyncClient()

    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.state.scheduler = scheduler

    yield

    scheduler.shutdown()
    await http_client.client.aclose()

app = FastAPI(title='Dashboard HTTP tools', lifespan=lifespan)

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
        port='8000', 
        loop='asyncio',
        reload=True
    )