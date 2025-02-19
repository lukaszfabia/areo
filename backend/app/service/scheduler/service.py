from typing import Dict, Optional
from app.db.models.model import Time
from app.db.crud import DB
from app.db.models.user import User
from app.service.raspberrypi.service import RaspberryPiService
from app.db.models.weather import Weather


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

    async def get_schedules(self) -> Optional[Dict[Time, str]]:
        """Get sorted times for 24h cycle

        returns:
            - time and reader email
        """
        read_times = await self.__db.get_times(User, "email")
        return read_times

    async def make_read(self, reader: str) -> Optional[Weather]:
        print(f"MAKE READ by {reader}")

        read = self.__raspberry.get_weather(reader)
        if read:
            res = await self.__db.create(model=read)
            return res
        return None
