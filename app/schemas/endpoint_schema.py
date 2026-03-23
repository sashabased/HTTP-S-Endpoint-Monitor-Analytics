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