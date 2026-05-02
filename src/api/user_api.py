from fastapi import APIRouter, Body, Depends, Form, HTTPException, Query, Request, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.limiter import limiter
from src.models.user import User
from src.schemas.user import TokenModel, UserRead, UserCreate
from src.db.session import open_session
from src.services import user_service
from src.services.auth import Hash, create_access_token, create_refresh_token, get_current_user, verify_refresh_token



router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(open_session)):
    create_user = await user_service.create_user(db, user)
    return UserRead.model_validate(create_user)

   
@router.post("/login", response_model=TokenModel)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(open_session)):
    return await user_service.authenticate_user(db, form_data)
 
   


@router.get("/me", response_model=UserRead)
@limiter.limit("5/minute")
async def read_current_user(request: Request, current_user: User = Depends(get_current_user)):
    
    return UserRead.model_validate(current_user)



@router.post("/refresh", response_model=TokenModel)
async def refresh_access_token(refresh_token: str = Form(...), db: Session = Depends(open_session)):
    return await user_service.refresh_token_service(refresh_token)


