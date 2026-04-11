from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI

import logging

from app.core.handlers import register_exception_handler
from app.core.logging import setup_logging
from app.routers import router
from app.database.session import db_manager

from contextlib import asynccontextmanager

setup_logging()
logger = logging.getLogger(__name__)

# Только для логирования
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    db_manager.init(os.getenv("DATABASE_URL"))
    yield

    await db_manager.close()
    logger.info("Application shutting down...")

app = FastAPI(title='Dashboard HTTP tools', lifespan=lifespan)
register_exception_handler(app)
app.include_router(router)