from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi import Depends
from pydantic import BaseModel

from app.jwt.jwt import AuthJWT
from app.db.models.user import User
from app.db.crud import DB
from app.routers.general import get_database

router = APIRouter()


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
        email=user["sub"],
    )

    if len(db_user) != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user[0]
