from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import config

import jwt

import redis.asyncio as aioredis


class RedisManger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False

        return cls.__instance

    def __init__(self, host: str = config.REDIS_HOST):
        if self.__initialized:
            return
        self._redis = aioredis.Redis(host=host, port=6379)
        self.__initialized = True

    async def setex(self, *args, **kwargs):
        return await self._redis.setex(*args, **kwargs)

    async def get(self, *args, **kwargs):
        return await self._redis.get(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self._redis.delete(*args)


class TokenManager(RedisManger):

    async def get_refresh(self, user_id: int) -> Optional[str]:
        refresh_token = await self.get(f"refresh_token:{user_id}")
        if refresh_token is not None:
            return refresh_token.decode("utf-8")
        return None

    async def delete_refresh(self, user_id: int) -> None:
        await self.delete(f"refresh_token:{user_id}")

    async def set_refresh(self, user_id: int, refresh: str) -> None:
        await self.setex(
            f"refresh_token:{user_id}", config.REFRESH_EXP_TIME, refresh
        )


def generate_jwt_token(user_id: int, exp_time: timedelta) -> str:
    expire = datetime.now(timezone.utc) + exp_time
    to_encode = {
        "exp": int(expire.timestamp()),
        "alg": config.JWT_ALGORITHM,
        "sub": str(user_id),
    }
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


def generate_access_token(user_id: int) -> str:
    return generate_jwt_token(user_id, config.ACCESS_EXP_TIME)


def generate_refresh_token(user_id: int) -> str:
    return generate_jwt_token(user_id, config.REFRESH_EXP_TIME)


def decode_jwt_token(token: str) -> Optional[int]:
    """
    :returns: if token is valid, returns "sub" value of decoded
    JWT token; if invalid, returns None
    """
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
    except jwt.exceptions.InvalidTokenError:
        return None
    return int(payload["sub"])


def generate_token_pair(user_id: int) -> Dict[str, str]:
    """
    generates access and refresh tokens for given email
    :returns: dictionary with keys "access_token" and "refresh_token",
    containing, respectively, access and refresh tokens
    """
    return {
        "access_token": generate_access_token(user_id),
        "refresh_token": generate_refresh_token(user_id),
    }
