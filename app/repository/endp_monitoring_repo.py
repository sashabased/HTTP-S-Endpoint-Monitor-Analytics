from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.core.exceptions import DatabaseError

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.exc import SQLAlchemyError

class CheckResultRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_endpoints_with_sites(self):

        active_endps = await self.session.scalars(
            select(Site)
            .join(Site.endpoints)
            .options(contains_eager(Site.endpoints))
            .where(Endpoint.is_active.is_(True))
        )

        return active_endps.unique().all() 
    

    async def bulk_save(self, results: list[CheckResult]):

        self.session.add_all(results)
        
        try:
            await self.session.commit()

            return results

        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Failed to bulk save data: {e}") # вместо логгера пока что

            return []