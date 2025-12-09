from tortoise import fields, models
from datetime import datetime

class Business(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    name = fields.CharField(max_length=100, unique=True, null=False, index=True)
    city = fields.CharField(max_length=255, null=False, default='Unspecified')
    country = fields.CharField(max_length=255, null=False, default='Unspecified')    
    business_description = fields.TextField(null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(auto_now=True)
    logo = fields.CharField(max_length=200, null=True)
    owner = fields.ForeignKeyField("models.User", related_name="business")