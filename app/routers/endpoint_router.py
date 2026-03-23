from fastapi import APIRouter, Request, Depends, HTTPException 

from app.database import db

from app import http_client
from app.services.endpoint_service import check_endpoint

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.endpoint_service import EndpointService
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, SiteRead

endpointer = APIRouter(
    prefix='/endpointer',
    tags=['url checker']
    )

@endpointer.post("/post-url")
async def get_user_url(user_input: SiteCreate, session: AsyncSession = Depends(db)):
    response = await EndpointService.post_user_url(user_input, session)
    
    if response is None:
        raise HTTPException(status_code=400, detail='error raised on same url trying to be added')
    elif response == 'url/endp':
        raise HTTPException(
            status_code=400, 
            detail='error raised on same url sended with /endpoint at the end'
        )
    return response
    
@endpointer.get("/sites/{id}")
async def get_url_by_id(site_id: int, session: AsyncSession = Depends(db)):
    response = await EndpointService.get_url_by_id(site_id, session)

    if response is None:
        raise HTTPException(status_code=400, detail='some error on user background')
    return response

# @endpointer.get("/start-check")
# async def check_url(request: Request, url: str):
#     scheduler = request.app.state.scheduler
    
#     response = scheduler.add_job(
#         check_endpoint,
#         "interval",
#         seconds=10,
#         args=[url]
#     )