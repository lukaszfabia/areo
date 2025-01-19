from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.crud import DB
from app.jwt.jwt import AuthJWT
from app.db.models.user import User
from app.utils.hash import hash_password
from fastapi import status

router = APIRouter(tags=["account", "user_management"])


class AuthModel(BaseModel):
    email: EmailStr
    password: str
    remember_me: Optional[bool] = None
    on_create: Optional[bool] = False


class AuthResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str


def get_database() -> DB:
    from app.main import app

    return app.mongo


@router.post(
    "/sign-in/",
    tags=["account", "user_management"],
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
async def sign_in(user: AuthModel, db: DB = Depends(get_database)):
    db_user = await db.filter(model=User, limit=1, email=user.email)
    if len(db_user) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    requested_user: User = db_user[0]
    if not requested_user.compare_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = AuthJWT.create_access_token(sub=requested_user.email)
    refresh_token = AuthJWT.create_refresh_token(sub=requested_user.email)

    return AuthResponse(
        user=requested_user, access_token=access_token, refresh_token=refresh_token
    )


@router.post(
    "/sign-up/",
    tags=["account", "user_management", "creating account", "register"],
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(user: AuthModel, db: DB = Depends(get_database)):
    if not user.on_create:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="No 'on_create' property or check spelling!",
        )

    result = await db.filter(model=User, email=user.email)
    if len(result) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists!"
        )

    new_user = User(email=user.email, password=hash_password(user.password))
    access_token = AuthJWT.create_access_token(sub=new_user.email)
    refresh_token = AuthJWT.create_refresh_token(sub=new_user.email)

    try:
        new_user.id = await db.create(new_user)
    except Exception as e:
        print(f"nie zwrocilo nowego objectid {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong during creating new user!",
        )

    return AuthResponse(
        user=new_user, access_token=access_token, refresh_token=refresh_token
    )
