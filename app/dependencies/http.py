import httpx as hx

from typing import AsyncGenerator


async def get_http_client() -> AsyncGenerator[hx.AsyncClient, None]:
    async with hx.AsyncClient as client:
        yield client