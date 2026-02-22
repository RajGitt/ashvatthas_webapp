from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base


class PaymentMethod(str, enum.Enum):
    UPI = "upi"
    GPAY = "gpay"
    PHONEPE = "phonepe"
    PAYTM = "paytm"
    CARD = "card"
    NET_BANKING = "net_banking"
    WALLET = "wallet"


class PaymentGateway(str, enum.Enum):
    RAZORPAY = "razorpay"
    STRIPE = "stripe"
    PAYPAL = "paypal"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    payment_gateway = Column(SQLEnum(PaymentGateway), nullable=False)
    transaction_id = Column(String, nullable=True)  # Gateway transaction ID
    razorpay_order_id = Column(String, nullable=True)  # For Razorpay
    razorpay_payment_id = Column(String, nullable=True)  # For Razorpay
    razorpay_signature = Column(String, nullable=True)  # For Razorpay
    stripe_payment_intent_id = Column(String, nullable=True)  # For Stripe
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    failure_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    order = relationship("Order", back_populates="payment")
