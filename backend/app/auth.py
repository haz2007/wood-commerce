import os
from datetime import datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "super_secure_lumber_secret_key_change_me"
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    user_id: int,
    role: str,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = {
        "user_id": user_id,
        "role": role
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt