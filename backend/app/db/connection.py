import motor.motor_asyncio
from decouple import config
import pytest

MONGO_URI = config("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()


@pytest.fixture
async def get_db():
    try:
        yield db
    finally:
        pass
