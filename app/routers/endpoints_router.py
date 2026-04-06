from fastapi import APIRouter, Depends, HTTPException 

from app.core.exceptions import NotFoundError
from app.dependencies.service import get_endpoint_service
from app.services.endpoints_service import EndpointService
from app.schemas.endpoint_schema import EndpointCreate, EndpointEdit, EndpointRead

from typing import List


endpoints = APIRouter(
    prefix='/endpoints',
    tags=['endpoint crud funcs']
    )


# ПЕРЕНЕСТИ В РОУТЫ САЙТОВ к юрлам

# @endpoints.post("/urls/{url_id}/endpoints")
# async def add_endp_to_url(
#     url_id: int, 
#     user_input: EndpointCreate, 
#     service: EndpointService = Depends(get_endpoint_service)
# ):

#     try:
#         response = await service.validate_endp_to_post(url_id, user_input)

#         return response
    
#     except InvalidUrlPathError:
#         raise HTTPException(status_code=400, detail="URL with this id dont exist")
    
#     except DatabaseError:
#         raise HTTPException(status_code=400, detail="URL alredy have this endpoint")


@endpoints.patch("/{endp_id}", response_model=EndpointRead)
async def patch_endp_by_id(
    endp_id: int, 
    user_input: EndpointEdit, 
    service: EndpointService = Depends(get_endpoint_service)
):

    try:
        response = await service.check_to_patch_endp(endp_id, user_input)

        return response
    
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    

@endpoints.delete("/{endp_id}", status_code=200)
async def delete_endp_by_id(endp_id: int, service: EndpointService  = Depends(get_endpoint_service)):

    try:
        response = await service.check_to_del_endp(endp_id)

        return response
    
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    

@endpoints.get("/{endp_id}", response_model=EndpointRead)
async def get_endp_by_id(endp_id: int, service: EndpointService = Depends(get_endpoint_service)):

    try:
        response = await service.validate_endp_get(endp_id)

        return response
    
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Endpoint not found")