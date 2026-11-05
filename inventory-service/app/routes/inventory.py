from fastapi import APIRouter, HTTPException, status
from app.database import db_manager
from app.models import StockUpdateSchema, StockReserveSchema, InventoryResponseSchema

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/set", response_model=InventoryResponseSchema)
async def set_stock(item: StockUpdateSchema):
    inventory_col = db_manager.db["inventory"]
    
    await inventory_col.update_one(
        {"_id": item.product_id},
        {"$set": {"quantity": item.quantity}},
        upsert=True
    )
    return InventoryResponseSchema(product_id=item.product_id, quantity=item.quantity)

@router.get("/{product_id}", response_model=InventoryResponseSchema)
async def get_stock(product_id: str):
    inventory_col = db_manager.db["inventory"]
    stock = await inventory_col.find_one({"_id": product_id})
    
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product stock record not found"
        )
    return InventoryResponseSchema(product_id=product_id, quantity=stock["quantity"])

@router.post("/reserve")
async def reserve_stock(reservation: StockReserveSchema):
    inventory_col = db_manager.db["inventory"]
    
    # Atomic check and deduct using find_one_and_update
    result = await inventory_col.find_one_and_update(
        {"_id": reservation.product_id, "quantity": {"$gte": reservation.quantity}},
        {"$inc": {"quantity": -reservation.quantity}},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock or product {reservation.product_id} not found"
        )
    
    return {
        "status": "reserved",
        "product_id": reservation.product_id,
        "remaining_quantity": result["quantity"]
    }