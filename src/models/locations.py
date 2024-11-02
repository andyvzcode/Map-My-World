from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

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