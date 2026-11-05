from pydantic import BaseModel, Field
from typing import Optional

class ProductBaseSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductResponseSchema(ProductBaseSchema):
    id: str = Field(..., description="Unique product identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_12345",
                "name": "Keychron M3 Mini",
                "description": "High polling rate wireless mouse",
                "price": 49.99,
                "category": "Peripherals"
            }
        }