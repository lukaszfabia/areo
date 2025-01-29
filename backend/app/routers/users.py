from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from fastapi import status
from fastapi import Depends
from pydantic import BaseModel, EmailStr

from app.jwt.jwt import AuthJWT
from app.db.models.user import Settings, User
from app.db.crud import DB
from app.routers.general import get_database, get_raspberry
from app.service.raspberrypi.service import RaspberryPiService

router = APIRouter(tags=["user assiciated endpoints", "user managment"])


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    settings: Optional[Settings] = None


@router.get(
    "/user/me/",
    tags=["account", "get my data"],
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def me(
    user: dict = Depends(AuthJWT.get_current_user), db: DB = Depends(get_database)
):
    db_user = await db.filter(
        model=User,
        limit=1,
        _id=user["sub"],
    )

    if len(db_user) != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user[0]


@router.put(
    "/user/me/",
    tags=["editing account", "settings"],
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def edit(
    body: UserUpdate = Body(...),
    user: dict = Depends(AuthJWT.get_current_user),
    db: DB = Depends(get_database),
):
    user = await me(user, db)

    if updated := await db.update(
        model=User, id=user.id, **body.dict(exclude_unset=True)
    ):
        return updated

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong"
    )


@router.delete(
    "/user/me/",
    tags=["delete account"],
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def delete(
    user: dict = Depends(AuthJWT.get_current_user), db: DB = Depends(get_database)
):

    db_user = await me(user, db)

    if deleted := await db.delete(model=User, _id=db_user.id):
        return deleted

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong",
    )


@router.get(
    "/user/rfid",
    tags=["rfid card", "auth"],
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def add_rfid(
    user: dict = Depends(AuthJWT.get_current_user),
    db: DB = Depends(get_database),
    raspberry: RaspberryPiService = Depends(get_raspberry),
):
    try:
        result = await raspberry.send_command(
            topic="command/rfid",
            message={"action": "start_rfid"},
            timeout=30,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect with raspberry pi ",
        )

    uid = result["uid"]

    uid = "to jest testowe uid"

    # fields to update
    db_user: User = await me(user, db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user with given credentials",
        )

    db_user.settings.rfid_uid = uid

    return await db.update(
        model=User, id=db_user.id, **db_user.dict(exclude_unset=True, exclude={"id"})
    )
