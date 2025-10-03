from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()

# In-memory storage for demo purposes
fake_users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "is_active": True},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "is_active": True},
]


@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    """Get all users"""
    return fake_users_db[skip : skip + limit]


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    """Get a specific user by ID"""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    # Check if email already exists
    for existing_user in fake_users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    new_id = max([user["id"] for user in fake_users_db], default=0) + 1
    new_user = {"id": new_id, "is_active": True, **user.dict()}
    fake_users_db.append(new_user)
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    """Update an existing user"""
    for i, existing_user in enumerate(fake_users_db):
        if existing_user["id"] == user_id:
            updated_user = existing_user.copy()
            updated_user.update(user.dict(exclude_unset=True))
            fake_users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    for i, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            deleted_user = fake_users_db.pop(i)
            return {"message": f"User '{deleted_user['name']}' deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
