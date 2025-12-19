from tortoise import fields, models
from datetime import datetime

class Product(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    category = fields.CharField(max_length=50, null=False, index=True)
    original_price = fields.DecimalField(max_digits=10, decimal_places=2, null=False)
    sale_price = fields.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount_percentage = fields.IntField(default=0)
    stock = fields.IntField(default=0)
    image = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True, index=True)
    business = fields.ForeignKeyField("models.Business", related_name="products")

    def calculate_sale_price(self):
        if self.discount_percentage and self.discount_percentage > 0:
            discount_amount = (self.original_price * self.discount_percentage) / 100
            self.sale_price = self.original_price - discount_amount
        else:
            self.sale_price = self.original_price
    
    async def save(self, *args, **kwargs):
        self.calculate_sale_price()
        await super().save(*args, **kwargs)