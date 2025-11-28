from tortoise import fields, models
from datetime import datetime

class User(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    username = fields.CharField(max_length=20, unique=True, null=False)
    email = fields.CharField(max_length=50, unique=True, null=False)
    password = fields.CharField(max_length=128, null=False)
    is_verified = fields.BooleanField(default=False)
    verification_token = fields.CharField(max_length=255, null=True)
    join_date = fields.DatetimeField(default=datetime.utcnow)

