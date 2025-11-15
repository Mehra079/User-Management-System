from typing import AsyncGenerator
from .database import AsyncSessionLocal

async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
