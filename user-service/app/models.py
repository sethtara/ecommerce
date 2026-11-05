import uuid
from pydantic import BaseModel, EmailStr, Field

class UserBaseSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    role: str = Field(default="customer")

class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=6)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(UserBaseSchema):
    id: str = Field(..., description="Unique user identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "role": "customer"
            }
        }