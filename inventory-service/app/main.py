from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes.inventory import router as inventory_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()

app = FastAPI(title="E-commerce Inventory Service", lifespan=lifespan)
app.include_router(inventory_router)

@app.get("/")
async def health_check():
    return {"status": "Inventory Service is running"}