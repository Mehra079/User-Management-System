from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_NAME: str = "FastAPI Async App"
    APP_VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
