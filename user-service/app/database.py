from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None

db_manager = DatabaseManager()

def connect_to_mongo():
    db_manager.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_manager.db = db_manager.client[settings.DB_NAME]
    print(f"User Service connected to MongoDB database: {settings.DB_NAME}")

def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        print("Closed User Service MongoDB connection.")