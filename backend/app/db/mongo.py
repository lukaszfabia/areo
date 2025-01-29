from typing import Any, Dict, List, Optional
from bson import ObjectId
from decouple import config
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from datetime import datetime, timezone, timedelta
from app.db.crud import DB, T
from app.utils.hash import hash_password
from app.db.models.model import Time
from models.weather import Weather
import random

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

    async def filter(
        self,
        model: T,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        **kwargs,
    ) -> List[T]:
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
        if v := query.get("_id"):
            query["_id"] = ObjectId(v)

        documents = await collection.find(query).skip(skip).to_list(length=limit)

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
            new_obj = await collection.find_one({"_id": res.inserted_id})
            return new_obj

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

        fields_to_update = {
            k: v
            for k, v in kwargs.items()
            if model.editable(field=k) and (v is not None or "")
        }

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

    async def get_times(self, model: T, value: str) -> Optional[Dict[Time, str]]:
        """Get sorted times to read"""

        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        fields = {field: 1 for field in [value, "settings.times"]}
        fields["_id"] = 0  # remove id
        query = {"deleted_at": None}

        cursor = collection.find(query, fields)

        result: Dict[Time, str] = {}
        async for document in cursor:
            if "settings" in document and "times" in document["settings"]:
                for time in document["settings"]["times"]:
                    time_value = Time(
                        hour=time["hour"],
                        minute=time["minute"],
                        second=time["second"],
                        millisecond=time["millisecond"],
                    )

                    if time_value not in result:
                        result[time_value] = document[value]

        return result if result else None

    async def dummy_weather(self, model: T, reader: str, limit: Optional[int] = 20) -> bool:
        """Inserts dummy weather data

        Args:
            limit (Optional[int], optional): how many docs you want. Defaults to 20.

        Returns:
            bool: operation status
        """

        collection: AsyncIOMotorCollection = self.db[model.__repr_name__]

        dummy_data = []
        for _ in range(limit):
            weather_entry = Weather(
                temperature=round(random.uniform(-10, 35), 1),
                humidity=random.randint(20, 100),
                pressure=round(random.uniform(950,1075), 1),
                altitude=random.randint(-100, 1000),
                reader=reader
            )
            dummy_data.append(weather_entry)
        
        res = await collection.insert_many(dummy_data)
        return bool(res.inserted_ids)
