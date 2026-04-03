from fastapi import APIRouter, Request, Depends, HTTPException 

from app import http_client
from app.services.endpoint_service import check_endpoint
from app.dependencies.db import get_db
from app.core.exceptions import DatabaseGetError, DatabaseError, EndpointIdError, DatabaseDeleteError, InvalidUrlPathError, InvalidUrlDomainError, InvalidUrlSchemeError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.services.endpoint_service import UrlService
from app.schemas.endpoint_schema import SiteCreate, SiteRead, EndpointCreate, SiteEdit, SiteReadAdvanced, EndpointEdit, EndpointRead

from typing import List

endpointer = APIRouter(
    prefix='/endpointer',
    tags=['url checker']
    )

# ТУТ ПО ЮРЛАМ!!!

@endpointer.post("/urls", response_model=SiteRead)
async def post_user_url(user_input: SiteCreate, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.validate_user_url(user_input)
        return response
    
    except InvalidUrlPathError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except InvalidUrlSchemeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except InvalidUrlDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Internal server error')

@endpointer.get("/urls", response_model=List[SiteRead])
async def get_all_urls(session = Depends(get_db)):
    response = await UrlService(session).validate_all_urls()
    
    return response
    
@endpointer.patch("/urls/{url_id}", response_model=SiteRead)
async def patch_url_by_id(url_id: int, user_input: SiteEdit, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.check_to_edit_url(url_id, user_input)

        return response
    
    except InvalidUrlPathError:
        raise HTTPException(status_code=404, detail="URL with this Id dont exist")
    
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Internal server error")

@endpointer.delete("/urls/{url_id}", status_code=200)
async def delete_url_by_id(url_id: int, session = Depends(get_db)):
    service = UrlService(session)
    
    try:
        response = await service.check_to_del_url(url_id)

        if response is None:
            raise HTTPException(status_code=404, detail="URL with this Id dont exist")

        return response
    
    except DatabaseDeleteError as e:
        raise HTTPException(500, detail='Server error during deletion')
    
# ТУТ ПО ЭНДПОИНТАМ ЮРЛОВ!!!

@endpointer.post("/urls/{url_id}/endpoints")
async def add_endp_to_url(
    url_id: int, 
    user_input: EndpointCreate, 
    session = Depends(get_db)
):
    service = UrlService(session)

    try:
        response = await service.validate_endp_to_post(url_id, user_input)

        return response
    
    except InvalidUrlPathError:
        raise HTTPException(status_code=400, detail="URL with this id dont exist")
    
    except DatabaseError:
        raise HTTPException(status_code=400, detail="URL alredy have this endpoint")
    
@endpointer.patch("/endpoints/{endp_id}", response_model=EndpointRead)
async def patch_endp_by_id(endp_id: int, user_input: EndpointEdit, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.check_to_patch_endp(endp_id, user_input)

        return response
    
    except InvalidUrlPathError:
        raise HTTPException(status_code=404, detail="Endpoint with this Id dont exist")
    
    except DatabaseError:
        raise HTTPException(status_code=400, detail="You cant add same endpoint to same URL")  
    
@endpointer.delete("/endpoints/{endp_id}", status_code=200)
async def delete_endp_by_id(endp_id: int, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.check_to_del_endp(endp_id)

        return response
    
    except DatabaseDeleteError:
        raise HTTPException(status_code=404, detail="Endpoint with this Id dont exist or already deleted")
    
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Internal server error")

@endpointer.get("/endpoints/{endp_id}", response_model=EndpointRead)
async def get_endp_by_id(endp_id: int, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.validate_endp_get(endp_id)

        return response
    
    except EndpointIdError:
        raise HTTPException(status_code=400, detail="Endpoint with this Id dont exist")
    
# ЭТОТ РОУТ НЕ ОТНОСИТСЯ НИ К КАКИМ ИЗ ДВУХ ВАРИАНТОВ ОН ОБЩИЙ

@endpointer.get("/urls/{url_id}", response_model=SiteReadAdvanced)
async def get_url_by_id(url_id: int, session = Depends(get_db)):
    service = UrlService(session)

    try:
        response = await service.validate_url(url_id)

        return response
    
    except DatabaseGetError:
        raise HTTPException(status_code=404, detail="URL with this Id dont exist")
    

# @endpointer.get("/start-check")
# async def check_url(request: Request, url: str):
#     scheduler = request.app.state.scheduler
    
#     response = scheduler.add_job(
#         check_endpoint,
#         "interval",
#         seconds=10,
#         args=[url]
#     )