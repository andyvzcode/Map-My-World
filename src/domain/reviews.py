import datetime
from typing import Optional

from pydantic import BaseModel, Field

from domain.categories import CategoryData
from domain.locations import LocationData


class ReviewBody(BaseModel):
    category_id: int
    location_id: int
    last_reviewed: datetime.date

    class Config:
        extra = "ignore"
        from_attributes = True


class ReviewData(ReviewBody):
    id: Optional[int] = Field(default=None)
    created_at: Optional[datetime.datetime] = Field(default=None)
    updated_at: Optional[datetime.datetime] = Field(default=None)
    deleted_at: Optional[datetime.datetime] = Field(default=None)
    location: LocationData = Field(default=None)
    category: CategoryData = Field(default=None)

    class Config:
        extra = "ignore"
        from_attributes = True
