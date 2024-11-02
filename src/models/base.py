from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    def mark_deleted(self):
        self.deleted_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
