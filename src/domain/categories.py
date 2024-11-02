import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBody(BaseModel):
    name: str

    class Config:
        extra = "ignore"
        from_attributes = True


class CategoryData(CategoryBody):
    id: Optional[int] = Field(default=None)
    created_at: Optional[datetime.datetime] = Field(default=None)
    updated_at: Optional[datetime.datetime] = Field(default=None)
    deleted_at: Optional[datetime.datetime] = Field(default=None)

    class Config:
        extra = "ignore"
        from_attributes = True
