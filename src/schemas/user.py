from pydantic import BaseModel, ConfigDict

from src.models import UserRole


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str