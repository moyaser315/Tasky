from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User
from app.utils.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(tags=["authentication"])


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
