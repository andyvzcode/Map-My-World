from sqlalchemy import Column, Float

from models.base import BaseModel


class Location(BaseModel):
    __tablename__ = "locations"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
