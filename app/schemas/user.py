from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="Username must be between 3 and 20 characters")
    email: EmailStr = Field(..., description="User email address")





class UserCreate(UserBase):
    password: str = Field(..., description="Password it should have least one uppercase letter", min_length=6)

    @field_validator("password")
    @classmethod
    def password_must_have_capital(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least one uppercase letter")
        return v


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Unique user identifier", gt=0)
    api_key: str = Field(..., description="User's API key for authentication", min_length=32)

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token for authentication", min_length=1)
    token_type: str = Field(default="bearer", description="Type of token", example="bearer")
    api_key: str = Field(..., description="User's API key", min_length=32)


class TokenData(BaseModel):
    user_id: int | None = None
