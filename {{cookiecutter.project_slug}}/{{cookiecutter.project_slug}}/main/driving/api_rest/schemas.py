"""API request and response schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    name: str
    description: str = ""


class ItemResponse(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
