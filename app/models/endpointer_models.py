from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import DateTime, String, Integer, ForeignKey, Boolean, func, UniqueConstraint

from datetime import datetime

from typing import List

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    base_url: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    endpoints: Mapped[List["Endpoint"]] = relationship(
        back_populates='site', 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Endpoint(Base):
    __tablename__ = "endpoints"

    __table_args__ = (UniqueConstraint('site_id', 'path', name='site_path_uc'), )

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str]
    sampling_interval: Mapped[int | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    method: Mapped[str] 
    timeout: Mapped[float]

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey('sites.id', ondelete="CASCADE"))
    site: Mapped["Site"] = relationship(back_populates='endpoints')

    results: Mapped[List["CheckResult"]] = relationship(
        back_populates='endpoint', 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
class CheckResult(Base):
    __tablename__ = 'check_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    status_code: Mapped[int]
    is_available: Mapped[bool]
    response_time: Mapped[float]
    error_details: Mapped[str | None] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    endpoint_id: Mapped[int] = mapped_column(ForeignKey('endpoints.id', ondelete="CASCADE"))
    endpoint: Mapped["Endpoint"] = relationship(back_populates='results')