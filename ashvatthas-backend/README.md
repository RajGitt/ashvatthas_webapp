# ASHWATHAS E-commerce Backend

Modern, high-performance e-commerce backend built with FastAPI, supporting user authentication, shopping cart, orders, and integrated payment processing with Razorpay (Indian payments) and Stripe (International payments).

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Product Management**: Products with variants (size, color, stock)
- **Shopping Cart**: Real-time cart management with stock validation
- **Order Processing**: Complete order workflow from creation to delivery
- **Payment Integration**: 
  - **Razorpay**: UPI, GPay, PhonePe, Paytm, Cards, Net Banking (India)
  - **Stripe**: International card payments
- **Address Management**: Multiple shipping addresses per user
- **Async Architecture**: High-performance async database queries
- **Type Safety**: Full Pydantic validation and type hints
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (for caching and sessions)

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb ashwathas_db

# Or using psql
psql -U postgres
CREATE DATABASE ashwathas_db;
\q
```

### 3. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required Environment Variables:**

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ashwathas_db

# Security
SECRET_KEY=your-super-secret-key-here-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Razorpay (Indian Payments)
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Stripe (International Payments)
STRIPE_PUBLIC_KEY=pk_test_your_public_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@ashwathas.com
```

### 4. Database Migration

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Visit: http://localhost:8000/api/docs for API documentation

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token

### Shopping Cart Endpoints

- `GET /api/v1/cart/` - Get user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{item_id}` - Update cart item quantity
- `DELETE /api/v1/cart/items/{item_id}` - Remove item from cart
- `DELETE /api/v1/cart/` - Clear entire cart

### Payment Endpoints

- `POST /api/v1/payments/create` - Create payment for order
- `POST /api/v1/payments/verify/razorpay` - Verify Razorpay payment
- `POST /api/v1/payments/confirm/stripe` - Confirm Stripe payment
- `GET /api/v1/payments/{payment_id}` - Get payment details

## 💳 Payment Integration

### Razorpay (Indian Market)

Supports:
- UPI (Google Pay, PhonePe, Paytm, BHIM)
- Debit/Credit Cards
- Net Banking
- Wallets

**Frontend Integration:**

```javascript
const { order_id, key_id, amount } = await createPayment(orderId);

const options = {
  key: key_id,
  amount: amount,
  currency: "INR",
  name: "ASHWATHAS",
  order_id: order_id,
  handler: async function (response) {
    await verifyPayment({
      razorpay_order_id: response.razorpay_order_id,
      razorpay_payment_id: response.razorpay_payment_id,
      razorpay_signature: response.razorpay_signature
    });
  }
};

const razorpay = new Razorpay(options);
razorpay.open();
```

### Stripe (International)

**Frontend Integration:**

```javascript
import { loadStripe } from '@stripe/stripe-js';

const stripe = await loadStripe('pk_test_your_public_key');
const { client_secret } = await createPayment(orderId);

const { error } = await stripe.confirmCardPayment(client_secret, {
  payment_method: {
    card: cardElement,
    billing_details: { name: 'Customer Name' }
  }
});

if (!error) {
  await confirmPayment(payment_intent_id);
}
```

## 🏗️ Project Structure

```
ashwathas-backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication
│   │   ├── cart.py       # Shopping cart
│   │   └── payments.py   # Payment processing
│   ├── core/             # Core functionality
│   │   ├── security.py   # JWT & password hashing
│   │   └── payment_gateway.py  # Payment integrations
│   ├── models/           # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── payment.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── tests/                # Test files
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)
- Secure payment signature verification

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🚢 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Use production database
- Use production payment keys
- Configure HTTPS
- Set proper CORS origins

## 📞 Support

For issues or questions:
- API Documentation: http://localhost:8000/api/docs
- Razorpay Docs: https://razorpay.com/docs/
- Stripe Docs: https://stripe.com/docs/

## 📄 License

Proprietary - ASHWATHAS © 2026

---

**Made with ❤️ for ASHWATHAS - Contemporary Living**
