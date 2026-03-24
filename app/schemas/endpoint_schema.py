from pydantic import BaseModel, Field

from typing import Optional
from datetime import datetime

class SiteCreate(BaseModel):
    url: str = Field(max_length=150)
    name: str = Field(max_length=150)

class SiteRead(SiteCreate):
    created_at: datetime
    id: int

class SiteEdit(BaseModel):
    name: Optional[str] = Field(max_length=150)

# валидация для эндпоинтов, обязательная

class EndpointCreate(BaseModel):
    path: str = Field(max_length=150)
    sampling_interval: Optional[int] = Field(
        ge=10, 
        le=999, 
        default=None
    )
    is_active: bool = Field(default=False)

class EndpointRead(EndpointCreate):
    id: int
    site_id: int

class EndpointEdit(BaseModel):
    path: Optional[str] = Field(max_length=150)
    sampling_interval: Optional[int] = Field(
        ge=10, 
        le=999, 
        default=None
    )
    is_active: Optional[bool] = Field(default=None)