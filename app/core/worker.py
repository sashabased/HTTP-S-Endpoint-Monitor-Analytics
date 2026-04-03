from app.database.session import session_maker
from app.services.endp_monitoring_service import MonitoringSerivce

async def run_monitoring_serivce():

    async with session_maker() as session:
        service = MonitoringSerivce(session)

        try:
            print("Worker started monitoring cycle")

            await service.check_to_ping_endps()
            print("Worker finished monitoring cycle")

        except Exception as e:
            print(f"Some error was raised on: {e}")