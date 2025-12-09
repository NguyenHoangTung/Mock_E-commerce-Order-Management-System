import pytest_asyncio
<<<<<<< HEAD

from app.core.config import settings
from app.models.product_model import Product

from .factory import BusinessFactory, UserFactory


@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123")
    response = await client.post("/api/v1/users/login", json={"identifier": user.email, "password": "password123"})
=======
from .factory import UserFactory, BusinessFactory
from app.models.product_model import Product

@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123")
    response = await client.post("/users/login", json={"identifier": user.email, "password": "password123"})
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
    token = response.json()["access_token"]
    return token, user

#@pytest.mark.asyncio
async def test_create_product_success(client, auth_token):
    token, user = auth_token
    business =  await BusinessFactory.create(owner=user)
    payload = {
        "name": "Laptop",
        "category": "Electronic",
        "original_price": 20000000,
        "discount_percentage": 10,
        "stock": 50,
        "image": "http://example.com/image.png",
        "business_id": str(business.id)
    }

    headers = {"Authorization": f"Bearer {token}"}
<<<<<<< HEAD
    response = await client.post("/api/v1/products", json=payload, headers=headers)
=======
    response = await client.post("/products/products", json=payload, headers=headers)
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["sale_price"] == '1.8E+7'
    assert await Product.filter(category="Electronic").exists()

#@pytest.mark.asyncio
async def test_create_product_unauthorized(client):
<<<<<<< HEAD
    response = await client.post("/api/v1/products", json={})
=======
    response = await client.post("/products/products", json={})
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
    assert response.status_code == 401 

#@pytest.mark.asyncio
async def test_get_products_list(client):
    user = await UserFactory.create()
    business = await BusinessFactory.create(owner=user)
    
    await Product.create(name="Prod 1", category="c1", original_price=100000, sale_price=80000, business=business)
    await Product.create(name="Prod 2", category="c2", original_price=200000, sale_price=150000, business=business)
<<<<<<< HEAD

    response = await client.get("/api/v1/products")

=======
    
    response = await client.get("/products/products")
    
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 