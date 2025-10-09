import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/app_db"
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
