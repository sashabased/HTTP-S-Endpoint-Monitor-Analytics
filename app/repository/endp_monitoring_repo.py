from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.core.exceptions import DatabaseError

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, cast, Interval
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload
from sqlalchemy.exc import SQLAlchemyError


class CheckResultRepository():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_active_endpoints(self):

        interval_calc = func.make_interval(secs=Endpoint.sampling_interval)

        subquery = (
            select(
                Endpoint.id.label("endpoint_id"),
                func.max(CheckResult.timestamp).label("last_ts")
            )
            .outerjoin(Endpoint.results)
            .group_by(Endpoint.id)
            .subquery()
        )

        query = await self.session.scalars(
            select(Endpoint)
            .join(subquery, Endpoint.id == subquery.c.endpoint_id)
            .options(joinedload(Endpoint.site))
            .where(
                or_(
                subquery.c.last_ts.is_(None),
                subquery.c.last_ts + interval_calc >= func.now()
                ),
                Endpoint.is_active.is_(True) 
            )
        )

        response = query.unique().all()

        return response
    

    async def bulk_save(self, results: list[CheckResult]):

        self.session.add_all(results)
        
        try:
            await self.session.commit()

            return results

        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Failed to bulk save data: {e}") # вместо логгера пока что

            return []