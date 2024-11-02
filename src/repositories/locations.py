from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.base import BaseRepository
from domain.locations import LocationBody, LocationData
from models.locations import Location as LocationModel


@dataclass
class LocationRepository(BaseRepository):
    session_maker: async_sessionmaker

    @property
    def base_query(self) -> Select:
        return select(LocationModel).filter(LocationModel.deleted_at.is_(None))

    async def get(self, location_id: int) -> Optional[LocationData]:
        async with self.session_maker() as session:
            query = self.base_query.filter(LocationModel.id == location_id)
            result = await session.execute(query)
            data = result.scalars().first()
        if not data:
            return None
        return LocationData.from_orm(data)

    async def save(self, location: LocationData) -> None:
        async with self.session_maker() as session:
            new_location = LocationModel(**location.dict())
            session.add(new_location)
            await session.commit()

        return LocationData.from_orm(new_location)

    async def update(self, location_id: int, location: LocationBody) -> None:
        async with self.session_maker() as session:
            query = self.base_query.filter(LocationModel.id == location_id)
            result = await session.execute(query)
            data = result.scalars().first()

            if not data:
                return None
            for key, value in location.dict().items():
                setattr(data, key, value)
            await session.commit()

        return LocationData.from_orm(data)

    async def delete(self, location_id: int) -> None:
        pass

    async def list(self) -> list[LocationData]:
        query = self.base_query
        async with self.session_maker() as session:
            result = await session.execute(query)
            data = result.scalars().all()

        return [LocationData.from_orm(location) for location in data if data]

    async def delete(self, location_id: int) -> None:
        async with self.session_maker() as session:
            query = self.base_query.filter(LocationModel.id == location_id)
            result = await session.execute(query)
            data = result.scalars().first()

            if not data:
                return None

            data.mark_deleted()
            await session.commit()
