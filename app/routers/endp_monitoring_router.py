from fastapi import APIRouter, Request, Depends, HTTPException 

from app import http_client
from app.services.endpoint_service import check_endpoint
from app.database import db
from app.core.exceptions import DatabaseGetError, DatabaseError, EndpointIdError, DatabaseDeleteError, InvalidUrlPathError, InvalidUrlDomainError, InvalidUrlSchemeError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.services.endpoint_service import UrlService
from app.schemas.endpoint_schema import SiteCreate, SiteRead, EndpointCreate, SiteEdit, SiteReadAdvanced, EndpointEdit, EndpointRead

from typing import List

from app.repository.endp_monitoring_repo import CheckResultRepository

endp_monitor = APIRouter(
    prefix='/endpoint_monitoring',
    tags=['checks endpoints of choosen url']
)

@endp_monitor.get("/urls/{url_id}/endpoints/stats")
async def get_all_active_endp(url_id: int, session = Depends(db)):
    response =  await CheckResultRepository(session).get_active_endpoints_with_sites(url_id)

    return response