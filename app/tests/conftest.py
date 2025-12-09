import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from unittest.mock import AsyncMock, patch
import os

os.environ["MAIL_USERNAME"] = "test_user"
os.environ["MAIL_PASSWORD"] = "test_password"
os.environ["MAIL_FROM"] = "test@example.com"
os.environ["MAIL_PORT"] = "587"
os.environ["MAIL_SERVER"] = "smtp.gmail.com"
os.environ["SECRET_KEY"] = "test_secret_key_for_jwt"
os.environ["DATABASE_URL"] = "sqlite://:memory:"
from app.main import app 

TORTOISE_TEST_CONFIG = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["app.models.user_model", "app.models.business_model", "app.models.product_model", "app.models.order_model", "aerich.models"],
            "default_connection": "default",
        },
    },
}

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_tests():
    await Tortoise.init(config=TORTOISE_TEST_CONFIG)
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()
    await Tortoise.close_connections()

@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
async def mock_email_sending():
    with patch("app.utils.email.FastMail.send_message", new_callable=AsyncMock) as mock_send:
        yield mock_send