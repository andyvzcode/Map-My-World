from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base import BaseModel


class LocationCategoryReviewed(BaseModel):
    __tablename__ = "location_category_reviewed"
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    last_reviewed = Column(Date, nullable=False)

    location = relationship("Location")
    category = relationship("Category")
