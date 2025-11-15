from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.database import engine, Base
from app.routers import auth as auth_router, users as users_router
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="User Management System", version="0.1.0")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created!")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth_router.router)
app.include_router(users_router.router)

@app.get("/ping")
async def ping():
    return {"ping": "pong"}
