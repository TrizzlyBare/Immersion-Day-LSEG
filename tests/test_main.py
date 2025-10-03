import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "healthy"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_read_items():
    """Test get all items"""
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_item():
    """Test create item"""
    item_data = {"name": "Test Item", "description": "A test item", "price": 9.99}
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert "id" in data


def test_read_item():
    """Test get specific item"""
    response = client.get("/api/v1/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_read_nonexistent_item():
    """Test get nonexistent item"""
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404
