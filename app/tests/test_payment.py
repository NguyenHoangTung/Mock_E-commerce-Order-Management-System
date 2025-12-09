import pytest, pytest_asyncio
from app.models import Order, Product
from .factory import UserFactory, BusinessFactory
from app.routes.payment_route import PAYMENT_SECRET_KEY

@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123")
    response = await client.post("/users/login", json={"identifier": user.email, "password": "password123"})
    token = response.json()["access_token"]
    return token, user

async def test_payment_webhook_success(client):
    user = await UserFactory.create()
    owner = await UserFactory.create()
    shop = await BusinessFactory.create(owner=owner)
    product = await Product.create(
        name = "Test Product",
        category = "Random",
        original_price = 100000,
        discount_percentage = 10,
        stock = 20,
        image = "http://example.com/image.png",
        business_id = str(shop.id)
    )
    order = await Order.create(
        user = user,
        shipping_address = "HN",
        total_amount = 10,
        status = "PENDING"
    )
    payload = {
        "order_id": str(order.id),
        "status": "SUCCESS",
        "transaction_id": "TRANS_123",
        "secret_key": PAYMENT_SECRET_KEY
    }
    response = await client.post("/payments/webhook", json=payload)
    assert response.status_code == 200
    order_updated = await Order.get(id=order.id)
    assert order_updated.status == "PAID"
    assert order_updated.transaction_id == "TRANS_123"

async def test_create_payment_url(client, auth_token):
    token, user = auth_token
    order = await Order.create(
        user = user,
        shipping_address = "HN",
        total_amount = 10,
        status = "PENDING"
    )
    headers = {"Authorization": f"Bearer {token}"}
    url = f"/payments/create-payment-url/{order.id}"
    response = await client.post(url, headers=headers)
    assert response.status_code == 200
    assert "payment_url" in response.json()