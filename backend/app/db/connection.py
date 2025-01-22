from typing import Any, List, Optional
from bson import ObjectId
from decouple import config
from pymongo.errors import WriteError
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from datetime import datetime, timezone


from app.db.crud import DB, T
from app.utils.hash import hash_password
from app.db.models.user import User


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
        query["deleted_at"] = None
        if query["_id"]:
            query["_id"] = ObjectId(query["_id"])

        documents = await collection.find(query).to_list(length=limit)

        return [model(**doc) for doc in documents]

    async def create(self, model: T) -> Optional[T]:
        """Create a new document in MongoDB

        Args:
            model (T): Model to insert

        Returns:
            Any: dict with new object
        """
        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        dumped = model.dict(by_alias=True)

        res = await collection.insert_one(dumped)
        if res.inserted_id:
            new_user = await collection.find_one({"_id": res.inserted_id})
            return new_user

        return None

    async def update(self, model: T, id: str, **kwargs) -> Optional[T]:
        """Update item in mongo db

        Args:
            model (T): Model to edit

        Returns:
            Any: is deleted successfullly
        """
        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        # use filters to find doc
        query = {"deleted_at": None, "_id": ObjectId(id)}

        now = datetime.now(timezone.utc)

        fields_to_update = {k: v for k, v in kwargs.items() if model.editable(field=k)}

        if p := fields_to_update.get("password"):
            fields_to_update["password"] = hash_password(p)

        operation = {"$set": {"updated_at": now, **fields_to_update}}

        result = await collection.update_one(query, operation)

        if result.modified_count > 0:
            updated_document = await collection.find_one(query)
            return model(**updated_document)

        return None

    async def delete(self, model: T, **kwargs) -> Optional[T]:
        """Soft delete from mongo db

        Args:
            model (T): Model to delete

        Returns:
            Any: is deleted successfullly
        """
        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        # use filters
        query = {k: v for k, v in kwargs.items()}
        query["deleted_at"] = None

        # update
        now = datetime.now(timezone.utc)
        operation = {"$set": {"deleted_at": now, "updated_at": now}}

        result = await collection.update_one(query, operation)

        if result.modified_count > 0:

            query.pop("deleted_at")

            updated_document = await collection.find_one(query)

            if updated_document:
                return model(**updated_document)

        return None
