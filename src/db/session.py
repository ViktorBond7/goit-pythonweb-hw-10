# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session

# from src.config.app_config import DATABASE_CONNECT_URL

# engine = create_engine(DATABASE_CONNECT_URL, connect_args={"autocommit": False})


# def open_session():
#     with Session(engine) as session:
#         yield session
import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

# from src.config.app_config import DATABASE_CONNECT_URL as DB_URL
from src.config.app_config import settings

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise  # Re-raise the original error
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.DATABASE_CONNECT_URL)


async def open_session():
    async with sessionmanager.session() as session:
        yield session