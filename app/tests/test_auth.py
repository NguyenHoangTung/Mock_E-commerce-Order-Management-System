import pytest
from app.models.user_model import User
from .factory import UserFactory


#@pytest.mark.asyncio
async def test_register_user(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",       
        "password": "password123"
    }
    response = await client.post("/users/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    user_db = await User.get(email=payload["email"])
    assert user_db is not None

#@pytest.mark.asyncio
async def test_login_user(client):
    password = "password123"
    user = await UserFactory.create(is_verified=True, password=password)
    payload = {
        "identifier": user.email,
        "password": password,
    }
    response = await client.post("/users/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

#@pytest.mark.asyncio
async def test_login_wrong(client):
    user = await UserFactory.create(password="password123")
    payload = {
        "identifier": user.email,
        "password": "wrong_password"
    }
    response = await client.post("users/login", json=payload)
    assert response.status_code == 401
