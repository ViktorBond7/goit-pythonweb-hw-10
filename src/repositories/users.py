from src.models.user import User
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
    async def get_user_by_email(self, email: str):
        result = self.db_session.query(User).filter(User.email == email).first()
        return result
    
    async def create_user(self, body: UserCreate, hashed_password: str = None, avatar: str = None) -> User:
        new_user = User(**body.model_dump(exclude_unset=True, exclude={"password"}), 
                        hashed_password=hashed_password, 
                        avatar=avatar)
        
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user