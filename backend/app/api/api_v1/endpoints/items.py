from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

# In-memory storage for demo purposes
fake_items_db = [
    {"id": 1, "name": "Apple", "description": "A red apple", "price": 1.50},
    {"id": 2, "name": "Banana", "description": "A yellow banana", "price": 0.75},
]


@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    """Get all items"""
    return fake_items_db[skip : skip + limit]


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Get a specific item by ID"""
    for item in fake_items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    """Create a new item"""
    new_id = max([item["id"] for item in fake_items_db], default=0) + 1
    new_item = {"id": new_id, **item.dict()}
    fake_items_db.append(new_item)
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item"""
    for i, existing_item in enumerate(fake_items_db):
        if existing_item["id"] == item_id:
            updated_item = existing_item.copy()
            updated_item.update(item.dict(exclude_unset=True))
            fake_items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    for i, item in enumerate(fake_items_db):
        if item["id"] == item_id:
            deleted_item = fake_items_db.pop(i)
            return {"message": f"Item '{deleted_item['name']}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
