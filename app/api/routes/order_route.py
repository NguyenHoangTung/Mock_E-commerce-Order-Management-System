import json

from fastapi import APIRouter, Depends, HTTPException
from tortoise.transactions import in_transaction

from app.api.deps import get_current_user
from app.core import redis_client
from app.models import Order, OrderItem, Product, User
from app.schemas.order_schema import CartItemResponse, CreateOrder, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_in: CreateOrder,
    current_user: User = Depends(get_current_user)
):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Nothing in cart.")
    
    redis = redis_client.get_redis_client()

    product_map = {}
    missing_products = []

    for item in order_in.items:
        cached_key = f"product:{item.product_id}"
        cached_data = await redis.get(cached_key)

        if cached_data:
            p_data = json.loads(cached_data)
            product_map[str(item.product_id)] = p_data
        else:
            missing_products.append(item.product_id)
    
    if missing_products:
        products = await Product.filter(id__in=missing_products).all()
        for product in products:
            product_map[str(product.id)] = {
                "id": str(product.id),
                "name": product.name,
                "sale_price": float(product.sale_price),
                "stock": product.stock
            }
            cached_key = f"product:{product.id}"
            await redis.set(cached_key, json.dumps(product_map[str(product.id)]), ex=3600)
    
    if len(product_map) != len(order_in.items):
        raise HTTPException(status_code=400, detail="One or more products do not exist.")
    
    async with in_transaction() as connection:
        order = await Order.create(
            user = current_user,
            shipping_address = order_in.shipping_address,
            total_amount = 0,
            using_db = connection
        )

        product_ids = [item.product_id for item in order_in.items]
        products = await Product.filter(id__in=product_ids).select_for_update().using_db(connection).all()

        if len(products) != len(order_in.items):
            raise HTTPException(status_code=400, detail="One or more products do not exist.")    

        product_map = {p.id: p for p in products}
        total_bill = 0
        response_items = []
        order_items_to_create = [] 
        products_to_update = []
        cache_keys_to_delete = []

        for item in order_in.items:
            product = product_map.get(item.product_id)
            if item.quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {product.name}."
                )
            item_price = product.sale_price * item.quantity
            total_bill += item_price

            order_item = OrderItem(
                order = order,
                product = product,
                quantity = item.quantity,
                price = item_price
            )
            order_items_to_create.append(order_item)

            product.stock -= item.quantity
            products_to_update.append(product)

            response_items.append(
                CartItemResponse(
                    product_id = str(product.id),
                    product_name = product.name,
                    quantity = item.quantity,
                    price = item_price
                )
            )
            cache_keys_to_delete.append(f"product:{product.id}")

        await OrderItem.bulk_create(order_items_to_create, using_db=connection)
        await Product.bulk_update(products_to_update, fields=["stock"], using_db=connection)     
        order.total_amount = total_bill
        await order.save(using_db=connection)   
    
    if cache_keys_to_delete:
        async with redis.pipeline() as pipe:
            for key in cache_keys_to_delete:
                pipe.delete(key)
            await pipe.execute()

    return OrderResponse(
        id = order.id,
        status = order.status,
        total_amount = order.total_amount,
        shipping_address = order.shipping_address,
        created_at = order.created_at,
        items = response_items
    )
