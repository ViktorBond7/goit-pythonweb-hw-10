from datetime import datetime, timedelta, UTC, timezone
from typing import Optional
from urllib import response

from fastapi import Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.models.user import User
from src.config import app_config as config
from src.db.session import open_session


from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# class Hash:
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#     def verify_password(self, plain_password, hashed_password):
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def get_password_hash(self, password: str):
#         return self.pwd_context.hash(password)

class Hash:
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password) -> bool:
        return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# define a function to generate a new access token
def create_access_token(data: dict)-> str:
    issue_date_time = datetime.now(timezone.utc)
    expire_date_time = issue_date_time + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire_date_time = issue_date_time + timedelta(seconds=30)
    # header = {'alg': config.ALGORITHM}
    payload = {**data, "iat": issue_date_time, "exp": expire_date_time, "type": "access"}
   
    res = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    
    return res


def create_refresh_token(data: dict) -> str:
    issue_date_time = datetime.now(timezone.utc)
    expire_date_time = issue_date_time + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {**data, "iat": issue_date_time, "exp": expire_date_time, "type": "refresh"}
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(open_session)
):
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("Token received in get_current_user87878787787878787:", token)
    try:
        # Decode JWT
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        
        email = payload["sub"]
        if email is None or payload.get("type") != "access":
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user_service = await db.execute(
        select(User).filter(User.email == email)
    )
    user_service = user_service.scalar_one_or_none()
    if user_service is None:
        raise credentials_exception
    
    return user_service


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(open_session)
# ):
   
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     print("Token received in get_current_user87878787787878787:", token)
#     try:
#         # Decode JWT
#         payload = jwt.decode(
#             token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
#         )
        
#         email = payload["sub"]
#         if email is None or payload.get("type") != "access":
#             raise credentials_exception
#     except JWTError as e:
#         raise credentials_exception
#     user_service = db.query(User).filter(User.email == email).first()
    
#     if user_service is None:
#         raise credentials_exception
    
#     return user_service

def verify_refresh_token(token: str) -> Optional[str] | None:
    try:
        
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        
        email = payload.get("sub")
        
        type_ = payload.get("type")
        
        if email is None or type_ != "refresh":
            return None
        return email
    except JWTError:
        return None

# def set_token_cookie(response: Response, access_token: str, refresh_token: str):
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         secure=False,
#         samesite="lax",
#         max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,

#     )
#     response.set_cookie(
#         key="refresh_token",
#         value=refresh_token,
#         httponly=True,
#         secure=False,
#         samesite="lax",
#         max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
#     )

# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(open_session)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         # Decode JWT
#         payload = jwt.decode(
#             token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
#         )
#         username = payload["sub"]
#         if username is None:
#             raise credentials_exception
#     except JWTError as e:
#         raise credentials_exception
#     user_service = UserService(db)
#     user = await user_service.get_user_by_username(username)
#     if user is None:
#         raise credentials_exception
#     return user


