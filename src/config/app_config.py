# DATABASE_CONNECT_URL = "postgresql+psycopg://admin:password@localhost:5433/db_contacts"
# DATABASE_CONNECT_URL = "postgresql+asyncpg://admin:password@localhost:5433/db_contacts"
# SECRET_KEY = "secret_key"
# ALGORITHM = "HS256"
from pydantic import EmailStr
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

    MAIL_USERNAME: EmailStr = "example@meta.ua"
    MAIL_PASSWORD: str = "secretPassword"
    MAIL_FROM: EmailStr = "example@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLD_NAME: str
    CLD_API_KEY: int 
    CLD_API_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()



# from fastapi import BackgroundTasks, FastAPI
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
# from pydantic import BaseModel, EmailStr
# from starlette.responses import JSONResponse



# class EmailSchema(BaseModel):
#     email: List[NameEmail]  # Supports both "user@example.com" and "Name <user@example.com>" formats


# conf = ConnectionConfig(
#     MAIL_USERNAME ="username",
#     MAIL_PASSWORD = "**********",
#     MAIL_FROM = "test@email.com",
#     MAIL_PORT = 465,
#     MAIL_SERVER = "mail server",
#     MAIL_STARTTLS = False,
#     MAIL_SSL_TLS = True,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )

# @app.post("/email")
# async def simple_send(email: EmailSchema) -> JSONResponse:

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=email.dict().get("email"),  # Can include "Name <email@domain.com>" format
#         body=html,
#         subtype=MessageType.html)

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})    