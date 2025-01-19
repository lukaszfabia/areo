from pydantic import BaseModel
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta


class Settings(BaseModel):
    authjwt_secret_key: str = config("JWT_SECRET")
    authjwt_algorithm: str = config("JWT_ALGO")
    access_token_expiration: int = timedelta(seconds=60 * 60 * 24)  # 24h
    refresh_token_expiration: timedelta = timedelta(
        seconds=60 * 60 * 24 * 30
    )  # 1 month


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

settings = Settings()
