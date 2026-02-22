from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.product import ProductVariant, Product
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's shopping cart."""
    
    # Get cart with items
    result = await db.execute(
        select(Cart)
        .where(Cart.user_id == current_user.id)
        .options(
            selectinload(Cart.items).selectinload(CartItem.product_variant).selectinload(ProductVariant.product)
        )
    )
    cart = result.scalar_one_or_none()
    
    if not cart:
        # Create cart if it doesn't exist
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
    
    # Calculate totals and enrich items with product details
    total_items = 0
    total_price = 0.0
    enriched_items = []
    
    for item in cart.items:
        variant = item.product_variant
        product = variant.product
        
        item_price = product.base_price + variant.price_adjustment
        total_items += item.quantity
        total_price += item_price * item.quantity
        
        enriched_item = CartItemResponse(
            id=item.id,
            product_variant_id=item.product_variant_id,
            quantity=item.quantity,
            added_at=item.added_at,
            product_name=product.name,
            product_image=product.image_url,
            size=variant.size,
            color=variant.color,
            price=item_price
        )
        enriched_items.append(enriched_item)
    
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=enriched_items,
        total_items=total_items,
        total_price=total_price,
        created_at=cart.created_at,
        updated_at=cart.updated_at
    )


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add item to shopping cart."""
    
    # Get user's cart
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()
    
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        await db.flush()
    
    # Check if product variant exists and has stock
    result = await db.execute(
        select(ProductVariant)
        .where(ProductVariant.id == item_data.product_variant_id)
        .options(selectinload(ProductVariant.product))
    )
    variant = result.scalar_one_or_none()
    
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found"
        )
    
    if variant.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {variant.stock_quantity}"
        )
    
    # Check if item already in cart
    result = await db.execute(
        select(CartItem)
        .where(
            CartItem.cart_id == cart.id,
            CartItem.product_variant_id == item_data.product_variant_id
        )
    )
    existing_item = result.scalar_one_or_none()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item_data.quantity
        if variant.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {variant.stock_quantity}"
            )
        existing_item.quantity = new_quantity
        cart_item = existing_item
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_variant_id=item_data.product_variant_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)
    
    await db.commit()
    await db.refresh(cart_item)
    
    # Enrich response with product details
    product = variant.product
    item_price = product.base_price + variant.price_adjustment
    
    return CartItemResponse(
        id=cart_item.id,
        product_variant_id=cart_item.product_variant_id,
        quantity=cart_item.quantity,
        added_at=cart_item.added_at,
        product_name=product.name,
        product_image=product.image_url,
        size=variant.size,
        color=variant.color,
        price=item_price
    )


@router.put("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: UUID,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update cart item quantity."""
    
    # Get cart item
    result = await db.execute(
        select(CartItem)
        .join(Cart)
        .where(
            CartItem.id == item_id,
            Cart.user_id == current_user.id
        )
        .options(
            selectinload(CartItem.product_variant).selectinload(ProductVariant.product)
        )
    )
    cart_item = result.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock
    if cart_item.product_variant.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {cart_item.product_variant.stock_quantity}"
        )
    
    cart_item.quantity = item_data.quantity
    await db.commit()
    await db.refresh(cart_item)
    
    # Enrich response
    variant = cart_item.product_variant
    product = variant.product
    item_price = product.base_price + variant.price_adjustment
    
    return CartItemResponse(
        id=cart_item.id,
        product_variant_id=cart_item.product_variant_id,
        quantity=cart_item.quantity,
        added_at=cart_item.added_at,
        product_name=product.name,
        product_image=product.image_url,
        size=variant.size,
        color=variant.color,
        price=item_price
    )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove item from cart."""
    
    result = await db.execute(
        select(CartItem)
        .join(Cart)
        .where(
            CartItem.id == item_id,
            Cart.user_id == current_user.id
        )
    )
    cart_item = result.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    await db.delete(cart_item)
    await db.commit()
    
    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Clear all items from cart."""
    
    result = await db.execute(
        select(Cart)
        .where(Cart.user_id == current_user.id)
        .options(selectinload(Cart.items))
    )
    cart = result.scalar_one_or_none()
    
    if cart:
        for item in cart.items:
            await db.delete(item)
        await db.commit()
    
    return None
