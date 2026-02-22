'''import razorpay
import stripe
from typing import Dict, Any
from app.config import settings

# Initialize Razorpay client (for Indian payments - UPI, GPay, etc.)
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

# Initialize Stripe (for International payments)
stripe.api_key = settings.STRIPE_SECRET_KEY


class RazorpayService:
    """Service for Razorpay payment integration (Indian market)."""
    
    @staticmethod
    def create_order(amount: float, currency: str = "INR", receipt: str = None) -> Dict[str, Any]:
        """
        Create a Razorpay order.
        
        Args:
            amount: Amount in smallest currency unit (paise for INR)
            currency: Currency code (default: INR)
            receipt: Unique receipt ID
            
        Returns:
            Dict containing order details
        """
        amount_in_paise = int(amount * 100)  # Convert to paise
        
        order_data = {
            "amount": amount_in_paise,
            "currency": currency,
            "receipt": receipt or f"order_{int(datetime.now().timestamp())}",
            "payment_capture": 1  # Auto capture
        }
        
        order = razorpay_client.order.create(data=order_data)
        return order
    
    @staticmethod
    def verify_payment_signature(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> bool:
        """
        Verify Razorpay payment signature.
        
        Returns:
            True if signature is valid, False otherwise
        """
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
    
    @staticmethod
    def fetch_payment(payment_id: str) -> Dict[str, Any]:
        """Fetch payment details from Razorpay."""
        return razorpay_client.payment.fetch(payment_id)
    
    @staticmethod
    def refund_payment(payment_id: str, amount: float = None) -> Dict[str, Any]:
        """
        Refund a payment.
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to refund (None for full refund)
            
        Returns:
            Refund details
        """
        if amount:
            amount_in_paise = int(amount * 100)
            return razorpay_client.payment.refund(payment_id, amount_in_paise)
        return razorpay_client.payment.refund(payment_id)


class StripeService:
    """Service for Stripe payment integration (International market)."""
    
    @staticmethod
    def create_payment_intent(
        amount: float,
        currency: str = "usd",
        metadata: Dict[str, Any] = None
    ) -> stripe.PaymentIntent:
        """
        Create a Stripe Payment Intent.
        
        Args:
            amount: Amount in smallest currency unit (cents for USD)
            currency: Currency code (default: USD)
            metadata: Additional data to attach
            
        Returns:
            PaymentIntent object
        """
        amount_in_cents = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True}
        )
        
        return intent
    
    @staticmethod
    def confirm_payment_intent(payment_intent_id: str) -> stripe.PaymentIntent:
        """Confirm a Payment Intent."""
        return stripe.PaymentIntent.confirm(payment_intent_id)
    
    @staticmethod
    def retrieve_payment_intent(payment_intent_id: str) -> stripe.PaymentIntent:
        """Retrieve a Payment Intent."""
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    
    @staticmethod
    def refund_payment(payment_intent_id: str, amount: float = None) -> stripe.Refund:
        """
        Refund a payment.
        
        Args:
            payment_intent_id: Stripe Payment Intent ID
            amount: Amount to refund (None for full refund)
            
        Returns:
            Refund object
        """
        refund_data = {"payment_intent": payment_intent_id}
        
        if amount:
            refund_data["amount"] = int(amount * 100)
        
        return stripe.Refund.create(**refund_data)
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, sig_header: str) -> bool:
        """
        Verify Stripe webhook signature.
        
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return True
        except stripe.error.SignatureVerificationError:
            return False


# Helper function to select payment service
def get_payment_service(gateway: str):
    """Get the appropriate payment service based on gateway."""
    if gateway == "razorpay":
        return RazorpayService()
    elif gateway == "stripe":
        return StripeService()
    else:
        raise ValueError(f"Unsupported payment gateway: {gateway}")
'''
from typing import Dict, Any
from app.config import settings

# Demo payment gateway implementations
# No real SDK imports needed for demo mode


class RazorpayService:
    """Demo Razorpay service - returns mock responses."""
    
    @staticmethod
    def create_order(amount: float, currency: str = "INR", receipt: str = None) -> Dict[str, Any]:
        """Create a demo Razorpay order."""
        return {
            "id": f"order_demo_{int(amount)}",
            "amount": int(amount * 100),
            "currency": currency,
            "receipt": receipt or "demo_receipt",
            "status": "created"
        }
    
    @staticmethod
    def verify_payment_signature(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> bool:
        """Demo signature verification - always returns True."""
        return True
    
    @staticmethod
    def fetch_payment(payment_id: str) -> Dict[str, Any]:
        """Fetch demo payment details."""
        return {
            "id": payment_id,
            "status": "captured",
            "method": "upi",
            "amount": 100000
        }


class StripeService:
    """Demo Stripe service - returns mock responses."""
    
    @staticmethod
    def create_payment_intent(
        amount: float,
        currency: str = "inr",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a demo Stripe Payment Intent."""
        return {
            "id": f"pi_demo_{int(amount)}",
            "client_secret": f"secret_demo_{int(amount)}",
            "amount": int(amount * 100),
            "currency": currency,
            "status": "requires_payment_method"
        }
    
    @staticmethod
    def retrieve_payment_intent(payment_intent_id: str) -> Dict[str, Any]:
        """Retrieve demo Payment Intent."""
        return {
            "id": payment_intent_id,
            "status": "succeeded",
            "amount": 100000,
            "currency": "inr"
        }






