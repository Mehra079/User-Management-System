from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

# Create user (plain password)
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password=user.password,  # store plain text
        role="user"
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Get user by email
async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(models.User).where(models.User.email == email))
    return res.scalars().first()

# Get user by ID
async def get_user(db: AsyncSession, user_id: int):
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    return res.scalars().first()

# Get multiple users
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    res = await db.execute(select(models.User).offset(skip).limit(limit))
    return res.scalars().all()
