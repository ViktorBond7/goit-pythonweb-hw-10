from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import TokenModel, UserRead, UserCreate, UserResponse, UserResponse
from src.db.session import open_session
from src.services import contact_service
from src.services.auth import Hash, create_access_token, get_current_user



router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(open_session)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
  
    new_user = User(
        email=user.email,
        password=Hash().get_password_hash(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserRead.model_validate(new_user)


@router.post("/login", response_model=TokenModel)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(open_session)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not Hash().verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = await create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    # return {"message": "Login successful"}


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    
    return UserResponse.model_validate(current_user)