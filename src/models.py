from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviews = relationship("LocationCategoryReview", back_populates="location")

    __table_args__ = (
        Index('idx_location_coords', 'latitude', 'longitude'),
    )

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviews = relationship("LocationCategoryReview", back_populates="category")
    
    __table_args__ = (
        Index('idx_category_name', 'name'),
    )

class LocationCategoryReview(Base):
    __tablename__ = "location_category_reviewed"
    
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    last_reviewed_at = Column(DateTime, default=datetime.utcnow)
    
    location = relationship("Location", back_populates="reviews")
    category = relationship("Category", back_populates="reviews")
    
    __table_args__ = (
        Index('idx_location_category', 'location_id', 'category_id'),
        Index('idx_last_reviewed', 'last_reviewed_at'),
    )