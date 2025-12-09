from app.models.user_model import User
from app.models.business_model import Business
from app.utils.password import get_password_hash
from faker import Faker
import uuid

fake = Faker()

class UserFactory:
    @staticmethod
    async def create(is_verified=True, password="password123") -> User:
        return await User.create(
            email=fake.email(),
            username=fake.user_name(),
            password=get_password_hash(password),
            is_verified=is_verified,
            is_active=True
        )

class BusinessFactory:
    @staticmethod
    async def create(owner: User) -> Business:
        return await Business.create(
            name=f"Shop {fake.company()}",
            id=str(uuid.uuid4()), 
            owner=owner,
            description="Test description"
        )