from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    LOGIN_URL: str
    CREATE_USER_URL: str


settings = Settings()
