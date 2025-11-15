from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from .core import settings
from .deps import get_async_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# -----------------------
# Password helpers (plain)
# -----------------------
def verify_password(plain_password: str, db_password: str) -> bool:
    return plain_password == db_password

# -----------------------
# Token helpers
# -----------------------
def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": str(subject), "role": role}
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# -----------------------
# Dependencies
# -----------------------
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = schemas.TokenData(sub=user_email, role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(db, token_data.sub)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def role_required(role: str):
    async def role_checker(current_user=Depends(get_current_active_user)):
        if current_user.role != role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_checker
