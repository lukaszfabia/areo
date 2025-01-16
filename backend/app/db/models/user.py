from pydantic import EmailStr
from typing import Optional
from model import Model


class Settings:
    device_token: str
    notifications: Optional[bool] = False
    notify_by_email: Optional[bool] = False


class User(Model):
    username: Optional[str] = None
    email: EmailStr
    password: str
    settings: Optional[Settings] = None
