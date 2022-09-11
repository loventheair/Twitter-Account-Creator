from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import UUID4
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from .schemas import TokenData
from typing import Optional

oauth2_schema = OAuth2PasswordBearer("/sign-in")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRAY = settings.expiray


def gen_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expiray = datetime.utcnow() + expire_delta
    else:
        expiray = datetime.utcnow() + timedelta(minutes=EXPIRAY)
    to_encode["exp"] = expiray
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_token(token: str, credentials_exception):
    try:
        encoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: UUID4 = encoded.get("sub")
        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token=token, credentials_exception=credentials_exception)
