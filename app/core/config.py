from typing import List

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "E-commerce API"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "5432"
    POSTGRES_DB: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PAYMENT_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()