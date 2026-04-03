from fastapi import APIRouter, Request, Depends, HTTPException 

from app.core.exceptions import DatabaseGetError, DatabaseError
from app.services.endp_monitoring_service import MonitoringSerivce
from app.repository.endp_monitoring_repo import CheckResultRepository
from app.dependencies.service import get_monitoring_service

from typing import List

endp_monitor = APIRouter(
    prefix='/endpoint_monitoring',
    tags=['checks endpoints of choosen url']
)

@endp_monitor.get("/urls/endpoints/stats")
async def get_all_active_endp(service: MonitoringSerivce = Depends(get_monitoring_service)):
    try:
        response = await service.check_to_ping_endps()

        return response
    
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Internal server error")