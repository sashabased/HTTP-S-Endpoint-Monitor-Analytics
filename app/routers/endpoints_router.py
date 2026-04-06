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


@endpoints.patch("/{endp_id}", response_model=EndpointRead)
async def patch_endp_by_id(
    endp_id: int, 
    user_input: EndpointEdit, 
    service: EndpointService = Depends(get_endpoint_service)
):

    return await service.update_endp(endp_id, user_input)


@endpoints.delete("/{endp_id}", status_code=200)
async def delete_endp_by_id(endp_id: int, service: EndpointService  = Depends(get_endpoint_service)):

    return await service.delete_endp(endp_id)
    

@endpoints.get("/{endp_id}", response_model=EndpointRead)
async def get_endp_by_id(endp_id: int, service: EndpointService = Depends(get_endpoint_service)):

    return await service.get_endpoint(endp_id)