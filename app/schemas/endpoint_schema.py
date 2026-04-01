from pydantic import BaseModel, Field

from typing import Optional, List
from datetime import datetime

class SiteCreate(BaseModel):
    base_url: str = Field(max_length=150)
    name: str = Field(max_length=150)

class SiteRead(SiteCreate):
    created_at: datetime
    id: int

class SiteEdit(BaseModel):
    name: Optional[str] = Field(max_length=150)

class SiteIdToDo(BaseModel):
    id: int 

# валидация для эндпоинтов, обязательная

class EndpointCreate(BaseModel):
    path: str = Field(max_length=150)
    sampling_interval: Optional[int] = Field(
        ge=10, 
        le=999, 
        default=None
    )
    is_active: bool = Field(default=False)
    method: str = Field(default="GET")
    timeout: float = Field(
        default=5.0,
        ge=0.1, 
        le=99.9
    )

class EndpointRead(EndpointCreate):
    id: int
    site_id: int

########################################
class SiteReadAdvanced(SiteCreate):
    created_at: datetime
    id: int
    endpoints: List[EndpointRead]
########################################

class EndpointEdit(BaseModel):
    path: Optional[str] = Field(max_length=150)
    sampling_interval: Optional[int] = Field(
        ge=10, 
        le=999, 
        default=None
    )
    is_active: Optional[bool] = Field(default=None)
    method: Optional[str] = None
    timeout: Optional[float] = Field(
        default=5.0,
        ge=0.1, 
        le=99.9
    )

# схемы валидаций для результатов проверки

class CheckResultRead(BaseModel):
    id: int
    status_code: int
    is_available: bool
    response_time: float
    error_details: Optional[str] = None
    timestamp: datetime

# схема с расширинной аналитикой

class EndpointWithHistory(EndpointRead):
    endp_res: List[CheckResultRead]