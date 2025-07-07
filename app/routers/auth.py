from fastapi import APIRouter, Depends, Body, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from typing import Annotated

router = APIRouter(tags=["authentication"])




@router.post(
    "/signup", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
    description="Register a new user with email and password. Returns user details and API key.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "User already exists"}
    }
)
async def signup(
    user: Annotated[UserCreate, Body(description="User registration data including email and password")], 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """
    Create a new user account.
    
    - **email**: Valid email address for the user
    - **password**: Password with at least 8 characters and one uppercase letter
    
    Returns the created user with their unique ID and API key.
    """
    db_user = await UserService.create_user(user, db)
    return db_user


@router.post(
    "/token", 
    response_model=Token,
    summary="Authenticate user and get access token",
    description="Login with username/email and password to receive JWT access token and API key.",
    responses={
        200: {"description": "Authentication successful"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Invalid request format"}
    }
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm, 
        Depends()
    ], 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    """
    Authenticate user and return access token.
    
    - **username**: User's email address
    - **password**: User's password
    
    Returns JWT access token, token type, and user's API key.
    """
    user, access_token = await UserService.authenticate_user(form_data, db)
    return Token(access_token=access_token, token_type="bearer", api_key=user.api_key)