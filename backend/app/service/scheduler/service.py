from app.db.crud import DB
from app.db.models.user import User


class SchedulerService:

    def __init__(self, db: DB):
        self.__db = db

    async def get_schedules(self):
        await self.__db.get_pair(User, "email", "times")

    async def make_read(self):
        pass
