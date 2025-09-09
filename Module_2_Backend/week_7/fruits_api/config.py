# Configuration settings for Fruits API
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()

@dataclass
class Settings:
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///fruits_api.db")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() == "true"
    
    # JWT settings
    JWT_PRIVATE_KEY_PATH: str = os.getenv("RSA_PRIVATE_KEY_PATH", "./private.pem")
    JWT_PUBLIC_KEY_PATH: str = os.getenv("RSA_PUBLIC_KEY_PATH", "./public.pem")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "30"))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRES_DAYS", "7"))

settings = Settings()
