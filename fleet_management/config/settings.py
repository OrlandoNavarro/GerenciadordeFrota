from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')


@dataclass
class Settings:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-me')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./fleet_management.db')
    ENV: str = os.getenv('ENV', 'development')


settings = Settings()
