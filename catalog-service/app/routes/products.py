import uuid
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import db_manager
from app.models import ProductCreateSchema, ProductResponseSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreateSchema):
    products_collection = db_manager.db["products"]
    
    product_id = f"prod_{uuid.uuid4().hex[:8]}"
    product_doc = {
        "_id": product_id,
        "name": product_in.name,
        "description": product_in.description,
        "price": product_in.price,
        "category": product_in.category
    }
    
    await products_collection.insert_one(product_doc)
    return ProductResponseSchema(id=product_id, **product_in.model_dump())

@router.get("/", response_model=List[ProductResponseSchema])
async def list_products():
    products_collection = db_manager.db["products"]
    products = await products_collection.find().to_list(100)
    
    return [
        ProductResponseSchema(
            id=prod["_id"],
            name=prod["name"],
            description=prod.get("description"),
            price=prod["price"],
            category=prod["category"]
        ) for prod in products
    ]

@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(product_id: str):
    products_collection = db_manager.db["products"]
    product = await products_collection.find_one({"_id": product_id})
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return ProductResponseSchema(
        id=product["_id"],
        name=product["name"],
        description=product.get("description"),
        price=product["price"],
        category=product["category"]
    )