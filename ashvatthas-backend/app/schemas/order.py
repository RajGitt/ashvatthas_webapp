from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.order import OrderStatus, PaymentStatus as OrderPaymentStatus
from app.models.payment import PaymentMethod, PaymentGateway, PaymentStatus


# Order Item Schemas
class OrderItemResponse(BaseModel):
    id: UUID
    product_variant_id: UUID
    quantity: int
    price_at_purchase: float
    
    # Additional fields from joins
    product_name: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Order Creation
class OrderCreate(BaseModel):
    shipping_address_id: UUID
    notes: Optional[str] = None


# Order Response
class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    total_amount: float
    status: OrderStatus
    payment_status: OrderPaymentStatus
    shipping_address_id: UUID
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


# Order Update (for admin)
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None


# Payment Schemas
class PaymentCreate(BaseModel):
    order_id: UUID
    payment_method: PaymentMethod
    payment_gateway: PaymentGateway


class RazorpayPaymentVerification(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class StripePaymentConfirmation(BaseModel):
    payment_intent_id: str


class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    payment_method: PaymentMethod
    payment_gateway: PaymentGateway
    transaction_id: Optional[str] = None
    amount: float
    currency: str
    status: PaymentStatus
    failure_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Gateway-specific fields
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    stripe_payment_intent_id: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Order List Response (with pagination)
class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
