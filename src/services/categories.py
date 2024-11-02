from typing import List, Optional

from domain.base import BaseCRUDService, BaseRepository
from domain.categories import CategoryBody, CategoryData


class CategoryService(BaseCRUDService):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def list(self) -> List[CategoryData]:
        return await self.repository.list()

    async def get(self, category_id: int) -> Optional[CategoryData]:
        return await self.repository.get(category_id)

    async def save(self, category: CategoryBody) -> Optional[CategoryData]:
        return await self.repository.save(category)

    async def update(
        self, category_id: int, category: CategoryBody
    ) -> Optional[CategoryData]:
        return await self.repository.update(category_id, category)

    async def delete(self, category_id: int) -> None:
        return await self.repository.delete(category_id)
