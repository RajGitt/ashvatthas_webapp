from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.payment import Payment, PaymentStatus, PaymentMethod, PaymentGateway
from app.schemas.order import (
    PaymentCreate,
    PaymentResponse,
    RazorpayPaymentVerification,
    StripePaymentConfirmation
)
from app.core.payment_gateway import RazorpayService, StripeService
from app.api.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create", response_model=dict)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a payment for an order.
    Returns payment details needed for frontend integration.
    """
    
    # Get order
    result = await db.execute(
        select(Order).where(
            Order.id == payment_data.order_id,
            Order.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.payment_status == "success":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already paid"
        )
    
    # Create payment record
    payment = Payment(
        order_id=order.id,
        payment_method=payment_data.payment_method,
        payment_gateway=payment_data.payment_gateway,
        amount=order.total_amount,
        currency="INR" if payment_data.payment_gateway == PaymentGateway.RAZORPAY else "USD"
    )
    
    db.add(payment)
    await db.flush()
    
    # Create payment with gateway
    gateway_response = {}
    
    if payment_data.payment_gateway == PaymentGateway.RAZORPAY:
        # Create Razorpay order
        razorpay_order = RazorpayService.create_order(
            amount=order.total_amount,
            currency="INR",
            receipt=f"order_{order.id}"
        )
        
        payment.razorpay_order_id = razorpay_order["id"]
        
        gateway_response = {
            "gateway": "razorpay",
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "key_id": settings.RAZORPAY_KEY_ID,  # Frontend needs this
            "payment_id": str(payment.id)
        }
    
    elif payment_data.payment_gateway == PaymentGateway.STRIPE:
        # Create Stripe Payment Intent
        payment_intent = StripeService.create_payment_intent(
            amount=order.total_amount,
            currency="usd",
            metadata={
                "order_id": str(order.id),
                "user_id": str(current_user.id)
            }
        )
        
        payment.stripe_payment_intent_id = payment_intent.id
        
        gateway_response = {
            "gateway": "stripe",
            "client_secret": payment_intent.client_secret,
            "payment_intent_id": payment_intent.id,
            "amount": payment_intent.amount,
            "currency": payment_intent.currency,
            "payment_id": str(payment.id)
        }
    
    await db.commit()
    
    return gateway_response


@router.post("/verify/razorpay", response_model=PaymentResponse)
async def verify_razorpay_payment(
    verification_data: RazorpayPaymentVerification,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify Razorpay payment signature and update payment status."""
    
    # Get payment by razorpay_order_id
    result = await db.execute(
        select(Payment)
        .join(Order)
        .where(
            Payment.razorpay_order_id == verification_data.razorpay_order_id,
            Order.user_id == current_user.id
        )
        .options(selectinload(Payment.order))
    )
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Verify signature
    is_valid = RazorpayService.verify_payment_signature(
        razorpay_order_id=verification_data.razorpay_order_id,
        razorpay_payment_id=verification_data.razorpay_payment_id,
        razorpay_signature=verification_data.razorpay_signature
    )
    
    if not is_valid:
        payment.status = PaymentStatus.FAILED
        payment.failure_reason = "Invalid payment signature"
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment verification failed"
        )
    
    # Update payment
    payment.razorpay_payment_id = verification_data.razorpay_payment_id
    payment.razorpay_signature = verification_data.razorpay_signature
    payment.status = PaymentStatus.SUCCESS
    payment.transaction_id = verification_data.razorpay_payment_id
    
    # Update order
    payment.order.payment_status = "success"
    payment.order.status = "confirmed"
    
    await db.commit()
    await db.refresh(payment)
    
    return payment


@router.post("/confirm/stripe", response_model=PaymentResponse)
async def confirm_stripe_payment(
    confirmation_data: StripePaymentConfirmation,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Confirm Stripe payment and update payment status."""
    
    # Get payment by payment_intent_id
    result = await db.execute(
        select(Payment)
        .join(Order)
        .where(
            Payment.stripe_payment_intent_id == confirmation_data.payment_intent_id,
            Order.user_id == current_user.id
        )
        .options(selectinload(Payment.order))
    )
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Retrieve payment intent from Stripe
    payment_intent = StripeService.retrieve_payment_intent(
        confirmation_data.payment_intent_id
    )
    
    if payment_intent.status == "succeeded":
        payment.status = PaymentStatus.SUCCESS
        payment.transaction_id = payment_intent.id
        payment.order.payment_status = "success"
        payment.order.status = "confirmed"
    elif payment_intent.status == "requires_payment_method":
        payment.status = PaymentStatus.FAILED
        payment.failure_reason = "Payment method failed"
    else:
        payment.status = PaymentStatus.PENDING
    
    await db.commit()
    await db.refresh(payment)
    
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get payment details."""
    
    result = await db.execute(
        select(Payment)
        .join(Order)
        .where(
            Payment.id == payment_id,
            Order.user_id == current_user.id
        )
    )
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment


from app.config import settings
