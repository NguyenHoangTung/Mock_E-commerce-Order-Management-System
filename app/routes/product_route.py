from fastapi import APIRouter, HTTPException, Depends
from app.models import Product, Business
from app.schemas.product_schema import ProductResponse, ProductUpdate, ProductCreate
from app.utils.dependency import get_current_user
from tortoise.expressions import Q
from typing import Optional



async def get_product_and_validate_owner(product_id: str, current_user=Depends(get_current_user)) -> Product:
    product = await Product.get_or_none(id=product_id).prefetch_related("business")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if product.business.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this product.")
    return product

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    current_user=Depends(get_current_user)
):
    business = await Business.get_or_none(id=product.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business is not existed.")
    if business.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized to add product to this business.")
    product_obj = await Product.create(
        name=product.name,
        category=product.category,
        original_price=product.original_price,
        discount_percentage=product.discount_percentage,
        stock=product.stock,
        image=product.image,
        business=business
    )
    return product_obj

@router.get("/products", response_model=list[ProductResponse])
async def get_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    business_name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 10,
    offset: int = 0,
):
    query = Product.filter(is_active=True).prefetch_related("business")
    if name:
        query = query.filter(name__icontains=name)
    if category:
        query = query.filter(category__icontains=category)
    if business_name:
        query = query.filter(business__name__icontains=business_name)
    if min_price is not None:
        query = query.filter(sale_price__gte=min_price)
    if max_price is not None:   
        query = query.filter(sale_price__lte=max_price)
    products = await query.limit(limit).offset(offset)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_detail(product_id: str):
    product = await Product.get_or_none(id=product_id, is_active=True).prefetch_related("business")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    product: Product = Depends(get_product_and_validate_owner)
):
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    product.is_active = True
    await product.save()
    return product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    product: Product = Depends(get_product_and_validate_owner)
):
    product.is_active = False
    await product.save()
    return {"detail": "Product deleted successfully."}