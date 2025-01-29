from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar
from app.db.models.model import Model, Time

T = TypeVar("T", bound=Model)


class DB(ABC):
    """An interface which must be implemented with every db. Use it to communicate with database"""

    @abstractmethod
    async def select(self, model: T) -> List[T]:
        """Select all records from table

        Args:
            model (T): type of the object
            limit - amount of fetched items
            skip - offset

        Returns:
            List[T]: result with objects
        """
        pass

    @abstractmethod
    async def filter(
        self,
        model: T,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        **kwargs
    ) -> List[T]:
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
    async def create(self, model: T) -> Optional[T]:
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

    @abstractmethod
    async def get_times(self, model: T, value: str) -> Optional[Dict[Time, str]]:
        """Get pair key - value

        Args:
            model (T): table
            args: fields that you want to have, first will be key

        Returns:
            Optional[Dict[str, Any]]: result
        """
        pass

    @abstractmethod
    async def dummy_weather(self, reader: str, limit: Optional[int] = 20) -> bool:
        """Generate some weather data

        Args:
            limit (Optional[int], optional): how much rows do u want to insert. Defaults to 20.

        Returns:
            bool: status
        """
        pass
