from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Product Variant Schemas
class ProductVariantCreate(BaseModel):
    size: str  # S, M, L, XL, XXL
    color: str
    stock_quantity: int = Field(..., ge=0)
    price_adjustment: float = 0.0
    sku: str


class ProductVariantResponse(BaseModel):
    id: UUID
    product_id: UUID
    size: str
    color: str
    stock_quantity: int
    price_adjustment: float
    sku: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProductVariantUpdate(BaseModel):
    size: Optional[str] = None
    color: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    price_adjustment: Optional[float] = None


# Product Schemas
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str
    base_price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    variants: List[ProductVariantCreate] = []


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    category: str
    base_price: float
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    variants: List[ProductVariantResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None


# Product List Response (with pagination)
class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
