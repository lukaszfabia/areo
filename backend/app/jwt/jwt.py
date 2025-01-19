import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from app.jwt.jwt_config import settings, oauth2_scheme


class AuthJWT:
    @staticmethod
    def __create_token(sub: str, expires_delta: timedelta):
        data = {"sub": sub}

        expire = datetime.now(timezone.utc) + expires_delta
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data, settings.authjwt_secret_key, algorithm=settings.authjwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_access_token(sub: str):
        return AuthJWT.__create_token(
            sub=sub, expires_delta=settings.access_token_expiration
        )

    @staticmethod
    def create_refresh_token(sub: str):
        return AuthJWT.__create_token(
            sub=sub, expires_delta=settings.refresh_token_expiration
        )

    @staticmethod
    def verify_access_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.authjwt_secret_key,
                algorithms=[settings.authjwt_algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def get_current_user(AuthJWT, token: str = Depends(oauth2_scheme)):
        return AuthJWT.verify_access_token(token)
