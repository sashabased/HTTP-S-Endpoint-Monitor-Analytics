from fastapi import APIRouter

from app.schemas.endpoint_schema import SiteCreate, SiteRead, SiteEdit, SiteReadAdvanced, EndpointCreate
from app.dependencies.service import SiteServiceDep

from typing import List


sites = APIRouter(
    prefix='/sites',
    tags=['url site checker']
    )


@sites.post("/", response_model=SiteRead)
async def post_user_url(
    user_input: SiteCreate, 
    service: SiteServiceDep
):

    response = await service.create_url(user_input)
    
    return response


@sites.get("/", response_model=List[SiteRead])
async def get_all_urls(service: SiteServiceDep):
    
    response = await service.get_urls()
    
    return response


@sites.patch("/{url_id}", response_model=SiteRead)
async def patch_url_by_id(
    url_id: int, 
    user_input: SiteEdit, 
    service: SiteServiceDep
):

    response = await service.update_url(url_id, user_input)

    return response
    

@sites.delete("/{url_id}", status_code=200)
async def delete_url_by_id(
    url_id: int, 
    service: SiteServiceDep
):

    await service.delete_url(url_id)

    return {"status": "deleted"}


@sites.get("/{url_id}", response_model=SiteReadAdvanced)
async def get_url_by_id(
    url_id: int, 
    service: SiteServiceDep
):

    response = await service.get_url(url_id)

    return response


@sites.post("/{url_id}/endpoints")
async def add_endp_to_url(
    url_id: int, 
    user_input: EndpointCreate, 
    service: SiteServiceDep
):

    response = await service.create_endpoint(url_id, user_input)

    return response