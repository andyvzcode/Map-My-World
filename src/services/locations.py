from typing import Optional

from domain.base import BaseCRUDService
from domain.locations import LocationBody, LocationData


class LocationService(BaseCRUDService):
    def __init__(self, repository) -> None:
        self.repository = repository

    async def list(self) -> list[LocationData]:
        return await self.repository.list()

    async def get(self, location_id: int) -> Optional[LocationData]:
        return await self.repository.get(location_id)

    async def save(self, location: LocationBody) -> Optional[LocationData]:
        return await self.repository.save(location)

    async def update(
        self, location_id: int, location: LocationBody
    ) -> Optional[LocationData]:
        return await self.repository.update(location_id, location)

    async def delete(self, location_id: int) -> None:
        return await self.repository.delete(location_id)
