from typing import Dict, List, Optional
from fastapi import APIRouter, Body, HTTPException, Query
from fastapi import status
from fastapi import Depends
from pydantic import BaseModel

from app.jwt.jwt import AuthJWT
from app.db.models.user import Settings, User
from app.db.crud import DB
from app.routers.general import get_database
from app.routers.general import get_raspberry
from app.service.raspberrypi.service import RaspberryPiService
from backend.app.db.models.weather import Weather
from app.routers.users import me

router = APIRouter(tags=["weather associated endpoints", "weather data"])


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int


class PaginatedWeather(BaseModel):
    data: List[Weather]
    pagination: PaginationInfo


@router.get(
    "/weather-history/",
    tags=["weather list", "get my weather data"],
    status_code=status.HTTP_200_OK,
    response_model=PaginatedWeather,
)
async def weather_historical_data(
    user: dict = Depends(AuthJWT.get_current_user),
    db: DB = Depends(get_database),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
):

    offset = (page - 1) * limit

    db_user: User = await me(user, db)

    data = await db.filter(
        model=Weather, limit=limit, skip=offset, reader=db_user.email
    )

    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No weather data"
        )

    total_items = len(data)

    return PaginatedWeather(
        data=data,
        pagination=PaginationInfo(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=(total_items + limit - 1) // limit,
        ),
    )


@router.get(
    "/weather/",
    tags=["current weather stats"],
    status_code=status.HTTP_201_CREATED,
    response_model=Weather,
)
async def current_weather(
    user: dict = Depends(AuthJWT.get_current_user),
    db: DB = Depends(get_database),
    raspberry: RaspberryPiService = Depends(get_raspberry),
):

    db_user: User = await me(user, db)

    weather = await raspberry.get_weather(reader=db_user.email)
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect with raspberry pi",
        )

    res = await db.create(weather)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create"
        )

    return res


# @router.get(
#     "/weather/notify/",
#     tags=["notify user"],
#     status_code=status.HTTP_200_OK,
# )
# async def notify(): ...
