import pytest, pytest_asyncio
from app.models.order_model import Order
from app.models.product_model import Product
from .factory import UserFactory, BusinessFactory

@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123")
    response = await client.post("/users/login", json={"identifier": user.email, "password": "password123"})
    token = response.json()["access_token"]
    return token, user

async def test_create_order_success(client, auth_token):
    token, user = auth_token
    owner = await UserFactory.create()
    shop = await BusinessFactory.create(owner=owner)
    product = await Product.create(
        name = "Test Product",
        category = "Random",
        original_price = 100000,
        discount_percentage = 10,
        stock = 10,
        image = "http://example.com/image.png",
        business_id = str(shop.id)
    )
    payload = {
        "items": [{"product_id": str(product.id), "quantity": 2}],
        "shipping_address": "123 Street"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/orders/", json = payload, headers = headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == '180000'
    prod_db = await Product.get(id=product.id)
    assert prod_db.stock == 8

async def test_create_order_fail(client, auth_token):
    token, user = auth_token
    owner = await UserFactory.create()
    business = await BusinessFactory.create(owner=owner)
    product = await Product.create(
        name = "Test Product",
        category = "Random",
        original_price = 100000,
        discount_percentage = 10,
        stock = 1,
        image = "http://example.com/image.png",
        business_id = str(business.id)
    )
    payload = {
        "items": [{"product_id": str(product.id), "quantity": 5}],
        "shipping_address": "123 Street"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/orders/", json = payload, headers = headers)
    assert response.status_code == 400