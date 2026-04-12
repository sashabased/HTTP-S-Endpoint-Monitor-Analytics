from fastapi import APIRouter

from app.dependencies.service import EndpointServiceDep
from app.schemas.endpoint_schema import EndpointEdit, EndpointRead


endpoints = APIRouter(
    prefix='/endpoints',
    tags=['endpoint crud funcs']
    )


@endpoints.patch("/{endp_id}", response_model=EndpointRead)
async def patch_endp_by_id(
    endp_id: int, 
    user_input: EndpointEdit, 
    service: EndpointServiceDep
):

    return await service.update_endp(endp_id, user_input)


@endpoints.delete("/{endp_id}", status_code=200)
async def delete_endp_by_id(
    endp_id: int, 
    service: EndpointServiceDep
):

    return await service.delete_endp(endp_id)
    

@endpoints.get("/{endp_id}", response_model=EndpointRead)
async def get_endp_by_id(
    endp_id: int, 
    service: EndpointServiceDep
):

    return await service.get_endpoint(endp_id)