# DATABASE_CONNECT_URL = "postgresql+psycopg://admin:password@localhost:5433/db_contacts"
# DATABASE_CONNECT_URL = "postgresql+asyncpg://admin:password@localhost:5433/db_contacts"
# SECRET_KEY = "secret_key"
# ALGORITHM = "HS256"
from pydantic_settings import BaseSettings, SettingsConfigDict
ACCESS_TOKEN_EXPIRE_MINUTES = 15 * 60

REFRESH_TOKEN_EXPIRE_DAYS = 7 * 24 * 60


class Settings(BaseSettings):
    DATABASE_CONNECT_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()