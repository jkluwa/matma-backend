from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    
    DB_HOST: str = "localhost"
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 3306

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
