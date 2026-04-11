from fastapi import APIRouter
from app.routers.endp_monitoring_router import endp_monitor
from app.routers.endpoints_router import endpoints
from app.routers.sites_router import sites

router = APIRouter()

router.include_router(endp_monitor)
router.include_router(endpoints)
router.include_router(sites)