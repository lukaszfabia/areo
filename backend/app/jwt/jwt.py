from bson import ObjectId
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from app.jwt.jwt_config import settings, oauth2_scheme


class AuthJWT:
    @staticmethod
    def __create_token(sub: str, expires_delta: timedelta):
        """Factory to make tokens, encodes info about obejct(user)

        Args:
            sub (str): info to encode
            expires_delta (timedelta): expire date

        Returns:
            bytes/str: token
        """
        data = {"sub": sub}

        expire = datetime.now(timezone.utc) + expires_delta
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data, settings.authjwt_secret_key, algorithm=settings.authjwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_access_token(sub: str | ObjectId):
        """Get new access token"""
        return AuthJWT.__create_token(
            sub=str(sub), expires_delta=settings.access_token_expiration
        )

    @staticmethod
    def create_refresh_token(sub: str | ObjectId):
        """Get new refresh token"""
        return AuthJWT.__create_token(
            sub=str(sub), expires_delta=settings.refresh_token_expiration
        )

    @staticmethod
    def __verify_access_token(token: str):
        """Checks expire state of the token

        Args:
            token (str): token to check

        Raises:
            HTTPException: Token has expired or Invalid token

        Returns:
            Mapping: payload
        """
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

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        """(Middleware) Validate current user

        Args:
            token (str, optional): incoming Bearer token. Defaults to Depends(oauth2_scheme).

        Returns:
            _type_: payload
        """
        return AuthJWT.__verify_access_token(token)
