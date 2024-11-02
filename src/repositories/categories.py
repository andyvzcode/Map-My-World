from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.base import BaseRepository
from domain.categories import CategoryData
from models.categories import Category as CategoryModel


@dataclass
class CategoryRepository(BaseRepository):
    session_maker: async_sessionmaker

    @property
    def base_query(self) -> Select:
        return select(CategoryModel).filter(CategoryModel.deleted_at.is_(None))

    async def get(self, location_id: int) -> Optional[CategoryData]:
        async with self.session_maker() as session:
            query = self.base_query.filter(CategoryModel.id == location_id)
            result = await session.execute(query)
            data = result.scalars().first()
        if not data:
            return None
        return CategoryData.from_orm(data)

    async def save(self, category: CategoryData) -> CategoryData:
        try:
            async with self.session_maker() as session:
                new_location = CategoryModel(**category.dict())
                session.add(new_location)
                await session.commit()
            return CategoryData.from_orm(new_location)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Category already exists")

    async def update(self, category_id: int, category: CategoryData) -> None:

        try:
            async with self.session_maker() as session:
                query = self.base_query.filter(CategoryModel.id == category_id)
                result = await session.execute(query)
                data = result.scalars().first()

                if not data:
                    return None
                for key, value in category.dict().items():
                    setattr(data, key, value)
                await session.commit()

        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Category already exists")

        return CategoryData.from_orm(data)

    async def delete(self, category_id: int) -> None:
        async with self.session_maker() as session:
            query = self.base_query.filter(CategoryModel.id == category_id)
            result = await session.execute(query)
            data = result.scalars().first()

            if not data:
                return None

            data.mark_deleted()
            await session.commit()

    async def list(self) -> list[CategoryData]:
        query = self.base_query
        async with self.session_maker() as session:
            result = await session.execute(query)
            data = result.scalars().all()

        return [CategoryData.from_orm(category) for category in data if data]
