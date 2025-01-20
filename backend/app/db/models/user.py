from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.models.model import Model
import bcrypt


class Settings(BaseModel):
    device_token: str
    notifications: Optional[bool] = False
    notify_by_email: Optional[bool] = False

    @classmethod
    def json_schema(cls, **kwargs):
        return {
            "type": "object",
            "properties": {
                "device_token": {"type": "string"},
                "notifications": {"type": "bool", "nullable": True, "default": False},
                "notify_by_email": {"type": "bool", "nullable": True, "default": False},
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
