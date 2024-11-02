from sqlalchemy import Column, String

from models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"
    name = Column(String, unique=True, nullable=False)
