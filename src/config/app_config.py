# DATABASE_CONNECT_URL = "postgresql+psycopg://admin:password@localhost:5433/db_contacts"
DATABASE_CONNECT_URL = "postgresql+asyncpg://admin:password@localhost:5433/db_contacts"
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15 * 60

REFRESH_TOKEN_EXPIRE_DAYS = 7 * 24 * 60
