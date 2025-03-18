from datetime import datetime, timezone
from typing import Any, Dict, Optional

import config

import jwt

import redis.asyncio as redis


class TokenManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host: str = "localhost"):
        self.redis = redis.Redis(host=host, port=6379)

    @staticmethod
    def generate_access_token(email: str) -> Dict[str, Any]:
        expire = datetime.now(timezone.utc) + config.ACCESS_EXP_TIME
        to_encode = {
            "exp": int(expire.timestamp()),
            "alg": config.JWT_ALGORITHM,
            "sub": email,
        }
        encoded_jwt = jwt.encode(
            to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
            )
        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.InvalidSignatureError,
            jwt.exceptions.InvalidKeyError,
        ):
            return None
        return payload["sub"]
