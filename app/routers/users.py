from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..deps import get_async_db
from ..auth import get_current_active_user, role_required

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserRead)
async def read_me(current_user=Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(role_required("admin"))
):
    return await crud.get_users(db, skip=skip, limit=limit)
