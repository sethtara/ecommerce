import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "ecommerce_user_db")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))

settings = Settings()