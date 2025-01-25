from pydantic import BaseModel, EmailStr
from typing import Any, List, Optional
from app.db.models.model import Model, Time
import bcrypt
from datetime import time


class Settings(BaseModel):
    """Denormalized table with settings, optional element of the user profile"""

    rfid_uid: Optional[str] = None  # card uid, must be unique
    device_token: Optional[str] = None  # uid of the device
    notifications: Optional[bool] = (
        False  # flag used to check if user wants to be notified
    )
    notify_by_email: Optional[bool] = False  # if user wants to be notifed by email

    times: Optional[List[Time]] = []  # read times

    @classmethod
    def json_schema(cls, **kwargs):
        return {
            "type": "object",
            "properties": {
                "rfid_uid": {"type": "string"},
                "device_token": {"type": "string"},
                "notifications": {"type": "bool", "nullable": True, "default": False},
                "notify_by_email": {"type": "bool", "nullable": True, "default": False},
                "times": {"type": "object", "nullable": True, "default": None},
            },
        }


class User(Model):
    username: Optional[str] = None
    email: EmailStr
    password: str
    settings: Optional[Settings] = None

    __repr_name__ = "users"

    def compare_password(self, password: str) -> bool:
        """Compares password with db

        Args:
            password (str): input password from login

        Returns:
            bool: is password the same
        """

        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
