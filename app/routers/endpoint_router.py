from fastapi import APIRouter, Request, Depends, HTTPException 

from app import http_client
from app.services.endpoint_service import check_endpoint
from app.database import db
from app.core.exceptions import DatabaseError, InvalidUrlPathError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.endpoint_service import UrlService
from app.schemas.endpoint_schema import SiteCreate, SiteEdit, SiteRead, EndpointCreate, EndpointEdit, EndpointRead

endpointer = APIRouter(
    prefix='/endpointer',
    tags=['url checker']
    )

@endpointer.post("/post-url")
async def post_user_url(user_input: SiteCreate, session = Depends(db)):
    service = UrlService(session)

    try:
        response = await service.validate_user_url(user_input)
        return response
    except InvalidUrlPathError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Internal server error')

@endpointer.get("/sites")
async def get_all_urls(session = Depends(db)):
    response = await UrlService(session).validate_all_urls()
    
    return response
    
# @endpointer.get("/sites/{id}")
# async def get_url_by_id(site_id: int, session: AsyncSession = Depends(db)):
#     response = await EndpointService.get_url_by_id(site_id, session)

#     if response is None:
#         raise HTTPException(status_code=400, detail='some error on user background')
#     return response

# # тут по эндпоинтам гоняем

# @endpointer.post("/sites/{endpoint:path}")
# async def add_endpoint_to_url(site_id: int, user_input: EndpointCreate, session: AsyncSession = Depends(db)):
#     response = await EndpointService.add_endpoint_to_url(site_id, user_input, session)
#     if response is None:
#         raise HTTPException(status_code=400, detail='error raised, cant add endpoint to url')
#     return response  

# @endpointer.get("/sites/{site_id}/endpoints/")
# async def get_all_site_endpoints(site_id: int, session: AsyncSession = Depends(db)):
#     response = await EndpointService.get_all_site_endpoints(site_id, session)
#     if response is None:
#         raise HTTPException(
#             status_code=400, 
#             detail='some error was raised on getting all endpoints'
#         )
#     return response

# @endpointer.get("/start-check")
# async def check_url(request: Request, url: str):
#     scheduler = request.app.state.scheduler
    
#     response = scheduler.add_job(
#         check_endpoint,
#         "interval",
#         seconds=10,
#         args=[url]
#     )