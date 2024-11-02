
from dataclasses import dataclass
from typing import Optional
from domain.base import BaseRepository
from sqlalchemy.ext.asyncio import async_sessionmaker
from models.locations import Location as LocationModel
from sqlalchemy import select
from domain.locations import LocationData

@dataclass
class LocationRepository(BaseRepository):
    session_maker: async_sessionmaker

    async def get(self, location_id: int) -> Optional[LocationData]:
        async with self.session_maker() as session:
            query = select(LocationModel).filter(LocationModel.id == location_id)
            result = await session.execute(query)
            data = result.scalars().first()
        if not data:
            return None
        return LocationData.from_orm(data)
    
    async def save(self, location: LocationData) -> None:
        pass

    async def update(self, location: LocationData) -> None:
        pass

    async def delete(self, location_id: int) -> None:
        pass

    async def list(self) -> None:
        pass
    
        