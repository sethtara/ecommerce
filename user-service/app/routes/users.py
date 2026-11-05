import uuid
from fastapi import APIRouter, HTTPException, status
from app.database import db_manager
from app.models import UserCreateSchema, UserLoginSchema, UserResponseSchema

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreateSchema):
    users_collection = db_manager.db["users"]
    
    existing_user = await users_collection.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user_id = str(uuid.uuid4())
    user_doc = {
        "_id": user_id,
        "name": user_in.name,
        "email": user_in.email,
        "role": user_in.role,
        "password": user_in.password
    }
    
    await users_collection.insert_one(user_doc)
    return UserResponseSchema(id=user_id, name=user_in.name, email=user_in.email, role=user_in.role)

@router.post("/login")
async def login_user(credentials: UserLoginSchema):
    users_collection = db_manager.db["users"]
    user = await users_collection.find_one({"email": credentials.email})
    
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {
        "message": "Login successful",
        "user_id": user["_id"],
        "role": user["role"]
    }

@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user_profile(user_id: str):
    users_collection = db_manager.db["users"]
    user = await users_collection.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponseSchema(
        id=user["_id"],
        name=user["name"],
        email=user["email"],
        role=user["role"]
    )

