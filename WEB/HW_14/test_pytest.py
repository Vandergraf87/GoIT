import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from .main import app
from api.models import get_db

@pytest.fixture
def client():
    client = TestClient(app)
    session = MagicMock(spec=Session)
    client.app.dependency_overrides[get_db] = lambda: session
    yield client
    client.app.dependency_overrides.clear()

def test_create_user_success(client):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == user_data["username"]

def test_create_existing_user(client):
    user_data = {
        "email": "existing@example.com",
        "password": "testpassword",
    }

    client.post("/users/", json=user_data)

    response = client.post("/users/", json=user_data)
    assert response.status_code == 409  
