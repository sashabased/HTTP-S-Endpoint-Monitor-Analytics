from fastapi import APIRouter
from app.dependencies.service import CheckResltServiceDep

endp_monitor = APIRouter(
    prefix='/endpoint_monitoring',
    tags=['checks endpoints of choosen url']
)


@endp_monitor.get("/urls/endpoints/stats")
async def get_all_active_endp(service: CheckResltServiceDep):

    return await service.check_to_ping_endps()


# Функция неактуальна вызывает метод репозитория, что не есть хорошо
# @endp_monitor.get("/endpoints")
# async def test_get(service: CheckResltServiceDep):

#     return await service.repo.get_active_endpoints()