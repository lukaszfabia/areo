from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from fastapi import status
from fastapi import Depends
from pydantic import BaseModel

from app.jwt.jwt import AuthJWT
from app.db.models.user import Settings, User
from app.db.crud import DB
from app.routers.general import get_database

router = APIRouter(tags=["weather associated endpoints", "weather data"])


# TODO: implement pagination
@router.get(
    "/weather-history/",
    tags=["weather list", "get my weather data"],
    status_code=status.HTTP_200_OK,
)
async def weather_historical_data(): ...


@router.get(
    "/weather/",
    tags=["current weather stats"],
    status_code=status.HTTP_200_OK,
)
async def current_weather(): ...


@router.get(
    "/weather/notify/",
    tags=["notify user"],
    status_code=status.HTTP_200_OK,
)
async def notify(): ...
