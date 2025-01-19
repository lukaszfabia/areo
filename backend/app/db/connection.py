from typing import Any, List, Optional
from decouple import config
from pymongo.errors import WriteError
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.db.crud import DB, T


class MongoDB(DB):
    def __init__(self) -> None:
        uri = config("MONGO_URI", default=None)
        db_name = config("MONGO_DB_NAME", default=None)

        if not uri:
            raise ValueError("Please provide MONGO_URI")
        if not db_name:
            raise ValueError("Please provide MONGO_DB_NAME")

        self.__client = AsyncIOMotorClient(uri)
        self.__db_name: str = db_name

    @property
    def db(self) -> AsyncIOMotorDatabase:
        """Returns the database instance."""
        return self.__client[self.__db_name]

    def close(self):
        """Closes connection with db"""
        self.__client.close()

    def health_check(self) -> bool:
        """Checks connection with the database."""
        try:
            self.__client.admin.command("ping")
            print("Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    async def select(self, model: T) -> List[T]:
        """Get all models from mongo

        Args:
            model (T): Model from db

        Returns:
            List[T]: List of T's
        """
        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        documents = await collection.find({"deleted_at": None}).to_list(length=None)

        return [model(**doc) for doc in documents]

    async def filter(self, model: T, limit: Optional[int] = None, **kwargs) -> List[T]:
        """Filter models based on query

        Args:
            model (T): Model from db
            **kwargs: Query parameters

        Returns:
            List[T]: List of T's
        """

        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        query = {k: v for k, v in kwargs.items()}
        query.update({"deleted_at": None})

        documents = await collection.find(query).to_list(length=limit)

        return [model(**doc) for doc in documents]

    async def create(self, model: T) -> Any:
        """Create a new document in MongoDB

        Args:
            model (T): Model to insert

        Returns:
            Any: ID of the inserted document
        """
        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        dumped = model.model_dump(by_alias=True)

        res = await collection.insert_one(dumped)
        if res.inserted_id is None:
            raise WriteError(f"Failed to insert document {dumped}")

        return res.inserted_id
