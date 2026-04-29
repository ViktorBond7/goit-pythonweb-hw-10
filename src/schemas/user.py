from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str
    

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str