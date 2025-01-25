from typing import Dict, List
from app.db.models.model import Time
from app.db.crud import DB
from app.db.models.user import User
from app.service.raspberrypi.serivce import RaspberryPiService


class SchedulerService:

    def __init__(self, db: DB, raspberry: RaspberryPiService):
        """Initializer for scheduler

        Args:
            db (DB): db interface
            raspberry (RaspberryPiService): raspberry pi machine
        """
        self.__db = db
        self.__raspberry = raspberry

    @property
    def update_time(self) -> int:
        return self.__update_time_sec

    async def get_schedules(self) -> Dict[str, List[Time]]:
        """Get sorted times for 24h cycle"""
        read_times = await self.__db.get_times(User, "email")
        return read_times

    async def make_read(self, reader: str):
        read = self.__raspberry.get_weather(reader)
        await self.__db.create(model=read)
