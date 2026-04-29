from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.app_config import DATABASE_CONNECT_URL

engine = create_engine(DATABASE_CONNECT_URL, connect_args={"autocommit": False})


def open_session():
    with Session(engine) as session:
        yield session
