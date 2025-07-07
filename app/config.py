from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = "sqlite+aiosqlite:///./tasks.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    class Config:
        env_file = ".env"


settings = Settings()
