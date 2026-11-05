from pydantic import BaseModel, Field
from typing import List

class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class OrderCreateSchema(BaseModel):
    user_id: str
    items: List[OrderItemSchema]

class OrderResponseSchema(BaseModel):
    id: str
    user_id: str
    items: List[OrderItemSchema]
    total_price: float
    status: str