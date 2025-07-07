from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    api_key: str



class Token(BaseModel):
    access_token: str
    token_type: str
    api_key: str


class TokenData(BaseModel):
    user_id: int | None = None
