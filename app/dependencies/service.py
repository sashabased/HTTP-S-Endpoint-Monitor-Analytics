from fastapi import Depends

from app.repository.endp_monitoring_repo import CheckResultRepository
from app.services.endp_monitoring_service import MonitoringSerivce
from app.dependencies.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession

def get_monitoring_service(session: AsyncSession = Depends(get_db)):
    repo = CheckResultRepository(session)

    return MonitoringSerivce(repo)