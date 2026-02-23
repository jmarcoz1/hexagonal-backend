"""SQLAlchemy ORM models."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID

from {{ cookiecutter.project_slug }}.main.driven.db.database import Base
from {{ cookiecutter.project_slug }}.main.domain.item import Item


def _utcnow():
    return datetime.now(timezone.utc)


class ItemModel(Base):
    """SQLAlchemy model for the items table."""

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    def to_domain(self) -> Item:
        """Convert ORM model to domain entity."""
        return Item(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
