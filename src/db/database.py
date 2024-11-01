from functools import cache

from settings.config import Settings as s
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


class DB:
    engine: Engine
    
    def __init__(
        self, engine: Engine, session: sessionmaker | None = None
    ) -> None:
        self.engine = engine
        self._session = session or sessionmaker(autoflush=False, bind=engine)

    @property
    def session(self) -> Session:
        return self._session()

def create_db() -> DB:
    engine = create_engine(
        s.DATABASE_URL, pool_size=10, isolation_level="AUTOCOMMIT"
    )
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    return DB(engine, SessionLocal)


@cache
def get_session_maker() -> async_sessionmaker:
    engine = create_async_engine(
        s.DATABASE_URL,
        pool_size=s.POSTGRES_POOL_SIZE,
        pool_pre_ping=True,
    )
    return async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )


Base = declarative_base()