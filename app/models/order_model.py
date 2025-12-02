from tortoise import models, fields
from . import User, Product

class Order(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='orders')
    status = fields.CharField(max_length=20, default="PENDING")
    total_amount = fields.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_address = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    class Meta:
        table = "order"

class OrderItem(models.Model):
    id = fields.UUIDField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='items')
    product = fields.ForeignKeyField('models.Product', related_name='order_items')
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=12, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta:
        table = "order_item"