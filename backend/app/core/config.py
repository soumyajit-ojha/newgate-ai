# backend/app/core/config.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Newgate AI"
    API: str = "/api"

    # Database (Postgres)
    DATABASE_URL: str

    # Supabase (Storage)
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str

    class Config:
        # Points to the .env file in the root directory
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
