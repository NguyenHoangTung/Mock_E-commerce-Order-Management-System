from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.transactions import in_transaction
from app.models import Order, OrderItem, Product, User
from app.schemas.order_schema import CreateOrder, CartItemResponse, OrderResponse
from app.utils.dependency import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_in: CreateOrder,
    current_user: User = Depends(get_current_user)
):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Nothing in cart.")
    async with in_transaction() as connection:
        order = await Order.create(
            user = current_user,
            shipping_address = order_in.shipping_address,
            total_amount = 0,
            using_db = connection
        )

        total_bill = 0
        response_items = []

        for item in order_in.items:
            product = await Product.filter(id=item.product_id).select_for_update().using_db(connection).first()
            if not product: raise HTTPException(status_code=404, detail="The item is not exist.")
            if product.stock < item.quantity: raise HTTPException(status_code=400, detail=f"The item '{product.name}' is out of stock. Remain in stock: {product.stock}.")
            product.stock -= item.quantity
            await product.save(using_db=connection)
            price = product.sale_price
            total = price * item.quantity
            total_bill += total

            order_item = await OrderItem.create(
                order = order,
                product = product,
                quantity = item.quantity,
                price = price,
                using_db = connection
            )

            response_items.append(CartItemResponse(
                product_id = product.id,
                product_name = product.name,
                quantity = item.quantity,
                price = price,
            ))

        order.total_amount = total_bill
        await order.save(using_db=connection)

    return OrderResponse(
        id = order.id,
        status = order.status,
        total_amount = order.total_amount,
        shipping_address = order.shipping_address,
        created_at = order.created_at,
        items = response_items
    )
