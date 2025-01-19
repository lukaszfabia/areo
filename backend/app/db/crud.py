from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar
from app.db.models.model import Model

T = TypeVar("T", bound=Model)


class DB(ABC):
    """An interface which must be implemented with every db"""

    @abstractmethod
    async def select(self, model: T) -> List[T]:
        pass

    @abstractmethod
    async def filter(self, model: T, limit: Optional[int] = None, **kwargs) -> List[T]:
        pass

    @abstractmethod
    async def create(self, model: T) -> Any:
        pass
