from dataclasses import dataclass
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from domain.base import BaseRepository
from domain.reviews import ReviewBody, ReviewData
from models.categories import Category
from models.locations import Location
from models.reviews import LocationCategoryReviewed


@dataclass
class ReviewRepository(BaseRepository):
    session_maker: async_sessionmaker

    @property
    def base_query(self) -> Select:
        return select(LocationCategoryReviewed).filter(
            LocationCategoryReviewed.deleted_at.is_(None)
        )

    async def list(self) -> Optional[List[ReviewData]]:
        query = self.base_query
        async with self.session_maker() as session:
            query = (
                select(LocationCategoryReviewed)
                .options(
                    joinedload(LocationCategoryReviewed.location),
                    joinedload(LocationCategoryReviewed.category),
                )
                .order_by(LocationCategoryReviewed.last_reviewed.asc())
            )
            result = await session.execute(query)
            data = result.scalars().all()

        return [ReviewData.from_orm(review) for review in data if data]

    async def save(self, review: ReviewBody) -> any:
        try:
            async with self.session_maker() as session:
                location = await session.get(Location, review.location_id)
                if not location:
                    raise HTTPException(status_code=404, detail="Location not found")

                category = await session.get(Category, review.category_id)
                if not category:
                    raise HTTPException(status_code=404, detail="Category not found")

                new_location = LocationCategoryReviewed(**review.dict())
                session.add(new_location)
                await session.commit()

            return ReviewData.from_orm(new_location)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Review already exists")

    async def update(self, *args, **kwargs) -> any:
        raise NotImplementedError

    async def delete(self, *args, **kwargs) -> any:
        raise NotImplementedError

    async def get(self, *args, **kwargs) -> any:
        raise NotImplementedError
