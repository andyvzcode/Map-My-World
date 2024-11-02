from typing import List, Optional

from domain.base import BaseCRUDService
from domain.reviews import ReviewBody, ReviewData
from repositories.reviews import ReviewRepository


class ReviewService(BaseCRUDService):
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def list(self) -> List[ReviewData]:
        return await self.repository.list()

    async def save(self, review: ReviewBody) -> Optional[ReviewData]:
        return await self.repository.save(review)

    async def get(self, *args, **kwargs) -> any:
        raise NotImplementedError

    async def update(self, *args, **kwargs) -> any:
        raise NotImplementedError

    async def delete(self, *args, **kwargs) -> any:
        raise NotImplementedError
