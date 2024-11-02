from abc import ABC, abstractmethod
from typing import List


class BaseRepository(ABC):
    @abstractmethod
    def save(self, any: any) -> any:
        pass

    @abstractmethod
    def get(self, id: str) -> any:
        pass

    @abstractmethod
    def list(self) -> List[any]:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, any: any) -> any:
        pass


class BaseCRUDService(ABC):
    @abstractmethod
    def save(self, any: any) -> any:
        pass

    @abstractmethod
    def get(self, id: str) -> any:
        pass

    @abstractmethod
    def list(self) -> List[any]:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, any: any) -> any:
        pass
