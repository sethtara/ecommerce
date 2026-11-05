from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes.users import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()

app = FastAPI(title="E-commerce User Service", lifespan=lifespan)

app.include_router(user_router)

@app.get("/")
async def health_check():
    return {"status": "User Service is running"}