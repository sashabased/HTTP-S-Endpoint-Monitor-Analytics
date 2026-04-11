import httpx as hx

from fastapi import Depends
from typing import AsyncGenerator, Annotated


async def get_http_client() -> AsyncGenerator[hx.AsyncClient, None]:
    async with hx.AsyncClient() as client:
        yield client

ClientSessionDep = Annotated[hx.AsyncClient, Depends(get_http_client)]