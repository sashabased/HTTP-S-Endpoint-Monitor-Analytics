from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.core.exceptions import DatabaseError

from typing import List

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload
from sqlalchemy.exc import SQLAlchemyError

import logging

logger = logging.getLogger(__name__)


class CheckResultRepository():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_active_endpoints(self):

        interval_calc = Endpoint.sampling_interval * text("INTERVAL '1 second'")

        last_check_subq = (
            select(func.max(CheckResult.timestamp))
            .where(CheckResult.endpoint_id == Endpoint.id)
            .correlate(Endpoint)
            .scalar_subquery()
        )

        query = await self.session.scalars(
            select(Endpoint)
            .options(joinedload(Endpoint.site))
            .where(
                Endpoint.is_active.is_(True),
                or_(
                    last_check_subq.is_(None),
                    last_check_subq + interval_calc <= func.now()
                )
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
            logger.exception(f"Failed to bulk save data") # теперь логгер

            return []