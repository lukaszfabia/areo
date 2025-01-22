from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar
from app.db.models.model import Model

T = TypeVar("T", bound=Model)


class DB(ABC):
    """An interface which must be implemented with every db. Use it to communicate with database"""

    @abstractmethod
    async def select(self, model: T) -> List[T]:
        """Select all records from table

        Args:
            model (T): type of the object

        Returns:
            List[T]: result with objects
        """
        pass

    @abstractmethod
    async def filter(self, model: T, limit: Optional[int] = None, **kwargs) -> List[T]:
        """Selects basing on filter

        Args:
            model (T): type of the object
            limit (Optional[int], optional): max element amount. Defaults to None.
            kwargs: filters

        Returns:
            List[T]: result with objects
        """
        pass

    @abstractmethod
    async def create(self, model: T) -> Any:
        """Insert new model to db

        Args:
            model (T): type of the object

        Returns:
            Any: returned value from db
        """
        pass

    @abstractmethod
    async def delete(self, model: T, **kwargs) -> Optional[T]:
        """Deletes one obejct from db

        Args:
            model (T): type of the object
            kwargs: filters
        Returns:
            Any: returned value from db
        """
        pass

    @abstractmethod
    async def update(self, model: T, id: str, **kwargs) -> Optional[T]:
        """Updates one obejct from db

        Args:
            model (T): type of the object
            kwargs: filters
        Returns:
            Any: returned value from db
        """
        pass
