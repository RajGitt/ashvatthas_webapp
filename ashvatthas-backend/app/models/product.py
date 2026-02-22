from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    size = Column(String, nullable=False)  # S, M, L, XL, XXL, etc.
    color = Column(String, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    price_adjustment = Column(Float, default=0.0)  # Additional price for this variant
    sku = Column(String, unique=True, nullable=False)  # Stock Keeping Unit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    product = relationship("Product", back_populates="variants")
    cart_items = relationship("CartItem", back_populates="product_variant")
    order_items = relationship("OrderItem", back_populates="product_variant")
