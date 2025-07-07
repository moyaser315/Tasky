import secrets
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated
from app.config import settings
from app.database import get_db
from app.schemas.user import TokenData
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_api_key():
    """Generate a secure API key."""
    return f"sk_{secrets.token_urlsafe(32)}"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

async def verify_api_key(x_api_key: str = Header(None), db: AsyncSession = Depends(get_db)):
    """Verify the API key belongs to a valid user."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key required"
        )
    
    # Check if API key exists in database
    result = await db.execute(
        select(User).where(User.api_key == x_api_key)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    return x_api_key

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    api_key: Annotated[str, Depends(verify_api_key)],
    db: AsyncSession = Depends(get_db)
):
    """Verify both JWT and API key belong to the same user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify JWT
    token_data = verify_access_token(token, credentials_exception)
    
    # Get user from JWT
    result = await db.execute(
        select(User).where(User.id == token_data.user_id)
    )
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    
    # Verify API key belongs to the same user
    if user.api_key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key does not match user"
        )
    
    return user