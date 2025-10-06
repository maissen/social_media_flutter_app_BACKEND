import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
