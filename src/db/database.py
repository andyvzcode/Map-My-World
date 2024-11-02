from functools import cache

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings.settings import settings


class DB:
    engine: create_async_engine

    def __init__(
        self, engine: create_async_engine, session: async_sessionmaker | None = None
    ) -> None:
        self.engine = engine
        self._session = session or async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )

    @property
    async def session(self) -> AsyncSession:
        async with self._session() as session:
            yield session


def create_db() -> DB:
    engine = create_async_engine(
        settings.DATABASE_URL, pool_size=10, isolation_level="AUTOCOMMIT"
    )
    SessionLocal = async_sessionmaker(
        autoflush=False, bind=engine, expire_on_commit=False
    )
    return DB(engine, SessionLocal)


@cache
def get_session_maker() -> async_sessionmaker:
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=settings.POSTGRES_POOL_SIZE,
        pool_pre_ping=True,
    )
    return async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )


Base = declarative_base()
