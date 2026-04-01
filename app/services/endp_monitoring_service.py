from app import http_client

import urllib.parse as ups

from app.core.exceptions import EndpointIdError, DatabaseGetError, InvalidUrlPathError, DatabaseError, InvalidUrlSchemeError, InvalidUrlDomainError, DatabaseDeleteError
from app.models.endpointer_models import Site, Endpoint, CheckResult
from app.schemas.endpoint_schema import SiteCreate, EndpointCreate, SiteEdit, EndpointEdit
from app.repository.endpoint_repo import UrlRepository

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class MonitoringSerivce():
    def __init__(self, session: AsyncSession):
        self.session = session