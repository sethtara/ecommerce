from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes.orders import router as order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))
app.include_router(order_router)

@app.get("/")
async def health_check():
    return {"status": "Order Service is running"}