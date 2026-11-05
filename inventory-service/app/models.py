from pydantic import BaseModel, Field

class StockUpdateSchema(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=0)

class StockReserveSchema(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class InventoryResponseSchema(BaseModel):
    product_id: str
    quantity: int