from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from fastapi import status
from fastapi import Depends
from pydantic import BaseModel, EmailStr

from app.jwt.jwt import AuthJWT
from app.db.models.user import Settings, User
from app.db.crud import DB
from app.routers.general import get_database

router = APIRouter()


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
