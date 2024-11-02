from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "map_my_world"
    SERVICE_NAME_DB: str = "database"
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{SERVICE_NAME_DB}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_POOL_SIZE: int = 10

    class Config:
        env_file = ".env"

settings = Settings()