from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    generate_api_key,
)


class UserService:
    @staticmethod
    async def create_user(user_create: UserCreate, db: AsyncSession):

        result = await db.execute(
            select(User).where(User.username == user_create.username)
        )
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Username already registered")

        result = await db.execute(select(User).where(User.email == user_create.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            api_key=generate_api_key(),
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def authenticate_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.username == form_data.username)
        )
        user = result.scalars().first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(data={"user_id": user.id})
        return user, access_token
