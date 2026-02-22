from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Cart Item Schemas
class CartItemCreate(BaseModel):
    product_variant_id: UUID
    quantity: int = Field(..., ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    id: UUID
    product_variant_id: UUID
    quantity: int
    added_at: datetime
    
    # Additional computed fields (from joins)
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    price: Optional[float] = None  # base_price + price_adjustment
    
    model_config = ConfigDict(from_attributes=True)


# Cart Schemas
class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemResponse] = []
    total_items: int = 0
    total_price: float = 0.0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
