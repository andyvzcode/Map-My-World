from typing import Optional
from domain.base import BaseService
from domain.locations import LocationData

class LocationService(BaseService):
    def __init__(self, repository)-> None:
        self.repository = repository

    async def list(self)-> any:
        return self.repository.list()

    async def get(self, location_id: int)-> Optional[LocationData]:
        return await self.repository.get(location_id)

    async def save(self, location: LocationData)-> any:
        return self.repository.save(location)

    async def update(self, location_id: int, location: LocationData) -> any:
        return self.repository.update(location_id, location)

    async def delete(self, location_id)-> any:
        return self.repository.delete(location_id)