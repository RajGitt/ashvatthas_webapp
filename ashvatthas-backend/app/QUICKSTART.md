# ASHWATHAS Backend - Quick Start Guide

## 🎯 Getting Payment Gateway Credentials

### Razorpay (For Indian Payments - UPI, GPay, etc.)

1. Go to https://razorpay.com/
2. Sign up for a test account
3. Navigate to Settings → API Keys
4. Generate Test Keys (Key ID and Key Secret)
5. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Test Cards for Razorpay:**
- Card Number: 4111 1111 1111 1111
- Any future expiry date
- Any CVV

### Stripe (For International Payments)

1. Go to https://stripe.com/
2. Sign up for a test account
3. Navigate to Developers → API Keys
4. Copy Publishable Key and Secret Key
5. Add to `.env`:
   ```
   STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx
   STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
   ```

**Test Cards for Stripe:**
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- Any future expiry, any CVV

## 💻 Complete Setup Commands

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create PostgreSQL database
createdb ashwathas_db

# 4. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 5. Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output to SECRET_KEY in .env

# 6. Initialize database
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 7. Run the server
uvicorn app.main:app --reload
```

## 🧪 Testing the API

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123",
    "full_name": "Test User",
    "phone_number": "+91 98765 43210"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Save the access_token from response!**

### 3. Get Cart (Authenticated)

```bash
curl -X GET http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📱 Frontend Integration Example

### React + Razorpay

```javascript
import axios from 'axios';

// 1. Create order and get payment details
const createPayment = async (orderId) => {
  const response = await axios.post(
    'http://localhost:8000/api/v1/payments/create',
    {
      order_id: orderId,
      payment_method: 'upi',
      payment_gateway: 'razorpay'
    },
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  return response.data;
};

// 2. Initialize Razorpay checkout
const handlePayment = async () => {
  const paymentData = await createPayment(orderId);
  
  const options = {
    key: paymentData.key_id,
    amount: paymentData.amount,
    currency: paymentData.currency,
    name: 'ASHWATHAS',
    description: 'Order Payment',
    order_id: paymentData.order_id,
    handler: async function (response) {
      // Verify payment on backend
      await axios.post(
        'http://localhost:8000/api/v1/payments/verify/razorpay',
        {
          razorpay_order_id: response.razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_signature: response.razorpay_signature
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );
      
      alert('Payment successful!');
    },
    prefill: {
      name: 'Customer Name',
      email: 'customer@example.com',
      contact: '+919876543210'
    },
    theme: {
      color: '#4a5f4e'
    }
  };
  
  const razorpay = new window.Razorpay(options);
  razorpay.open();
};

// Add Razorpay script to HTML
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
```

### React + Stripe

```javascript
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe('pk_test_your_public_key');

const CheckoutForm = () => {
  const stripe = useStripe();
  const elements = useElements();
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Create payment
    const { data } = await axios.post(
      'http://localhost:8000/api/v1/payments/create',
      {
        order_id: orderId,
        payment_method: 'card',
        payment_gateway: 'stripe'
      },
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
    
    // Confirm payment
    const result = await stripe.confirmCardPayment(data.client_secret, {
      payment_method: {
        card: elements.getElement(CardElement),
        billing_details: {
          name: 'Customer Name',
        },
      },
    });
    
    if (result.error) {
      alert(result.error.message);
    } else {
      // Confirm on backend
      await axios.post(
        'http://localhost:8000/api/v1/payments/confirm/stripe',
        {
          payment_intent_id: result.paymentIntent.id
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );
      
      alert('Payment successful!');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit" disabled={!stripe}>
        Pay Now
      </button>
    </form>
  );
};

// Wrap with Elements
<Elements stripe={stripePromise}>
  <CheckoutForm />
</Elements>
```

## 🎨 Frontend Integration with ASHWATHAS Site

To connect the backend with your frontend:

1. **Update Frontend URLs:**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api/v1';
   ```

2. **Add Axios Configuration:**
   ```javascript
   import axios from 'axios';
   
   const api = axios.create({
     baseURL: 'http://localhost:8000/api/v1',
   });
   
   // Add token to requests
   api.interceptors.request.use((config) => {
     const token = localStorage.getItem('access_token');
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });
   ```

3. **Connect Cart:**
   ```javascript
   // Add to cart
   const addToCart = async (variantId, quantity) => {
     await api.post('/cart/items', {
       product_variant_id: variantId,
       quantity: quantity
     });
   };
   
   // Get cart
   const getCart = async () => {
     const response = await api.get('/cart/');
     return response.data;
   };
   ```

## 🔧 Common Issues & Solutions

### Database Connection Error
```bash
# Make sure PostgreSQL is running
sudo service postgresql start

# Check connection
psql -U postgres -d ashwathas_db
```

### Redis Not Running (if using)
```bash
# Start Redis
redis-server
```

### Migration Errors
```bash
# Reset migrations
alembic downgrade base
alembic upgrade head
```

### Import Errors
```bash
# Make sure you're in the correct directory
cd /path/to/ashwathas-backend
source venv/bin/activate
```

## 📊 Database Schema Visualization

```
Users ──┬── Addresses
        ├── Cart ──── Cart_Items ──── Product_Variants ──── Products
        └── Orders ──┬── Order_Items ──── Product_Variants
                     └── Payments
```

## 🚀 Production Checklist

- [ ] Change `DEBUG=False` in .env
- [ ] Use production database
- [ ] Use production payment keys (live mode)
- [ ] Set strong `SECRET_KEY` (32+ characters)
- [ ] Configure HTTPS/SSL
- [ ] Set proper CORS origins
- [ ] Enable rate limiting
- [ ] Setup logging and monitoring
- [ ] Configure email service
- [ ] Backup database regularly
- [ ] Use environment-specific configs

## 📞 Support Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Razorpay Docs:** https://razorpay.com/docs/payments/
- **Stripe Docs:** https://stripe.com/docs/payments
- **Pydantic Docs:** https://docs.pydantic.dev/

---

**Happy Coding! 🎉**
