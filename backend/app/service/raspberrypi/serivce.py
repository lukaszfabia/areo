from abc import ABC, abstractmethod

from app.db.models.weather import Weather


class RaspberryPiService(ABC):
    """Layer responsible for communication between raspberry pi and weather endpoints"""

    @abstractmethod
    def auth_user(self):
        """Authentication user by RFID card"""
        pass

    @abstractmethod
    def get_weather(self, reader: str) -> Weather:
        """Get weather stats"""
        pass
