import os

from aiocache import caches
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "postgres")
    SERVICE_NAME_DB: str = os.environ.get("SERVICE_NAME_DB", "postgres")
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{SERVICE_NAME_DB}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_MAX_OVERFLOW: int = 20
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)
    SERVICE_NAME_DB: str = os.environ.get("SERVICE_NAME_DB", "database")
    SERVICE_REDIS: str = os.environ.get("SERVICE_REDIS", "redis")
    REDIS_URL: str = f"redis://{SERVICE_REDIS}:6379"


settings = Settings()


def cache_settings():
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.RedisCache",
                "endpoint": settings.SERVICE_REDIS,
                "port": settings.REDIS_PORT,
                "timeout": 1,
                "serializer": {"class": "aiocache   .serializers.JsonSerializer"},
            }
        }
    )
