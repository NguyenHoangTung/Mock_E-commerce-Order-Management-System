<<<<<<< HEAD
import pytest
import pytest_asyncio

from app.core.config import settings
from app.models import Order, Product

from .factory import BusinessFactory, UserFactory


@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123", is_verified=True)
    response = await client.post("/api/v1/users/login", json={"identifier": user.email, "password": "password123"})
=======
import pytest, pytest_asyncio
from app.models import Order, Product
from .factory import UserFactory, BusinessFactory
from app.routes.payment_route import PAYMENT_SECRET_KEY

@pytest_asyncio.fixture
async def auth_token(client):
    user = await UserFactory.create(password="password123")
    response = await client.post("/users/login", json={"identifier": user.email, "password": "password123"})
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
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
<<<<<<< HEAD
        "secret_key": settings.PAYMENT_SECRET_KEY
    }
    response = await client.post("/api/v1/payments/webhook", json=payload)
=======
        "secret_key": PAYMENT_SECRET_KEY
    }
    response = await client.post("/payments/webhook", json=payload)
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
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
<<<<<<< HEAD
    url = f"/api/v1/payments/create-payment-url/{order.id}"
=======
    url = f"/payments/create-payment-url/{order.id}"
>>>>>>> f9eb3c7 (test(routers): Add pytest tests)
    response = await client.post(url, headers=headers)
    assert response.status_code == 200
    assert "payment_url" in response.json()