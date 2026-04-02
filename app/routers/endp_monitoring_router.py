from fastapi import APIRouter, Request, Depends, HTTPException 

from app import http_client
from app.services.endpoint_service import check_endpoint
from app.database import db
from app.core.exceptions import DatabaseGetError, DatabaseError, EndpointIdError, DatabaseDeleteError, InvalidUrlPathError, InvalidUrlDomainError, InvalidUrlSchemeError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.services.endp_monitoring_service import MonitoringSerivce
from app.schemas.endpoint_schema import SiteCreate, SiteRead, EndpointCreate, SiteEdit, SiteReadAdvanced, EndpointEdit, EndpointRead

from typing import List

from app.repository.endp_monitoring_repo import CheckResultRepository

endp_monitor = APIRouter(
    prefix='/endpoint_monitoring',
    tags=['checks endpoints of choosen url']
)

@endp_monitor.get("/urls/endpoints/stats")
async def get_all_active_endp(session = Depends(db)):
    service = MonitoringSerivce(session)

    try:
        response = await service.check_to_ping_endps()

        return response
    
    except DatabaseGetError:
        raise HTTPException(status_code=404, detail="URL active endpoints not found or URL dont exist")
    
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Internal server error")