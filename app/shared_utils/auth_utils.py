from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError

from app.users.models import User
from app.config import Config


async def get_current_user(token: str) -> User:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_in: int = 3600):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=expires_in)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt
