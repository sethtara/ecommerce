import uuid
import httpx
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database import db_manager
from app.config import settings
from app.models import OrderCreateSchema, OrderResponseSchema

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreateSchema):
    orders_col = db_manager.db["orders"]

    async with httpx.AsyncClient() as client:
        # 1. Validate User
        user_res = await client.get(f"{settings.USER_SERVICE_URL}/users/{order_in.user_id}")
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="User validation failed or user does not exist")

        # 2. Fetch Catalog details & Calculate total price
        total_price = 0.0
        for item in order_in.items:
            product_res = await client.get(f"{settings.CATALOG_SERVICE_URL}/products/{item.product_id}")
            if product_res.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found in catalog")
            
            product_data = product_res.json()
            total_price += product_data["price"] * item.quantity

        # 3. Reserve Inventory Stock
        for item in order_in.items:
            reserve_res = await client.post(
                f"{settings.INVENTORY_SERVICE_URL}/inventory/reserve",
                json={"product_id": item.product_id, "quantity": item.quantity}
            )
            if reserve_res.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock reservation failed for item {item.product_id}"
                )

    # 4. Save Order
    order_id = f"order_{uuid.uuid4().hex[:8]}"
    order_doc = {
        "_id": order_id,
        "user_id": order_in.user_id,
        "items": [item.model_dump() for item in order_in.items],
        "total_price": total_price,
        "status": "COMPLETED"
    }
    
    await orders_col.insert_one(order_doc)
    return OrderResponseSchema(
        id=order_id,
        user_id=order_in.user_id,
        items=order_in.items,
        total_price=total_price,
        status="COMPLETED"
    )

@router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(order_id: str):
    orders_col = db_manager.db["orders"]
    order = await orders_col.find_one({"_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return OrderResponseSchema(
        id=order["_id"],
        user_id=order["user_id"],
        items=order["items"],
        total_price=order["total_price"],
        status=order["status"]
    )