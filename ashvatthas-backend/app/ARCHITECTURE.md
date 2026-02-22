# 🏗️ ASHWATHAS - System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USERS / CUSTOMERS                              │
│                     (Browse, Shop, Pay Online)                          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DOMAIN & DNS                                    │
│                                                                         │
│   ashwathas.com          →    Frontend (Vercel)                        │
│   www.ashwathas.com      →    Frontend (Vercel)                        │
│   api.ashwathas.com      →    Backend (Railway)                        │
│                                                                         │
└──────────────┬────────────────────────────────┬─────────────────────────┘
               │                                │
               │                                │
               ▼                                ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│     FRONTEND (VERCEL)        │    │    BACKEND (RAILWAY)         │
│                              │    │                              │
│  • ashwathas.html            │◄──►│  • FastAPI Application       │
│  • CSS/JavaScript            │    │  • REST API Endpoints        │
│  • Product Catalog           │    │  • Authentication (JWT)      │
│  • Shopping Cart UI          │    │  • Business Logic            │
│  • Checkout Forms            │    │                              │
│  • Payment Integration       │    │  API Endpoints:              │
│                              │    │  /auth/register              │
│  Technologies:               │    │  /auth/login                 │
│  • HTML5                     │    │  /cart/*                     │
│  • CSS3                      │    │  /orders/*                   │
│  • Vanilla JavaScript        │    │  /payments/*                 │
│  • Razorpay SDK              │    │  /products/*                 │
│  • Stripe SDK                │    │                              │
│                              │    │  Technologies:               │
│  FREE Tier:                  │    │  • Python 3.10+              │
│  • Unlimited sites           │    │  • FastAPI                   │
│  • Auto SSL                  │    │  • SQLAlchemy (ORM)          │
│  • CDN                       │    │  • Pydantic                  │
│  • Custom domain             │    │  • Alembic (migrations)      │
└──────────────┬───────────────┘    └──────────────┬───────────────┘
               │                                   │
               │                                   │
               │                                   ▼
               │                    ┌──────────────────────────────┐
               │                    │   DATABASE (SUPABASE)        │
               │                    │                              │
               │                    │  • PostgreSQL 14+            │
               │                    │  • User accounts             │
               │                    │  • Products & variants       │
               │                    │  • Shopping carts            │
               │                    │  • Orders & payments         │
               │                    │  • Addresses                 │
               │                    │                              │
               │                    │  Tables:                     │
               │                    │  • users                     │
               │                    │  • addresses                 │
               │                    │  • products                  │
               │                    │  • product_variants          │
               │                    │  • carts / cart_items        │
               │                    │  • orders / order_items      │
               │                    │  • payments                  │
               │                    │                              │
               │                    │  FREE Tier:                  │
               │                    │  • 500MB database            │
               │                    │  • Auto backups              │
               │                    │  • Direct SQL access         │
               │                    └──────────────────────────────┘
               │
               │
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      PAYMENT GATEWAYS                                    │
│                                                                          │
│  ┌─────────────────────────┐         ┌─────────────────────────┐       │
│  │   RAZORPAY (India)      │         │   STRIPE (International)│       │
│  │                         │         │                         │       │
│  │  • UPI (GPay, PhonePe)  │         │  • Credit Cards         │       │
│  │  • Cards                │         │  • Debit Cards          │       │
│  │  • Net Banking          │         │  • Apple Pay            │       │
│  │  • Wallets              │         │  • Google Pay           │       │
│  │  • EMI                  │         │  • Local methods        │       │
│  │                         │         │                         │       │
│  │  Currency: INR          │         │  Currency: USD/EUR/etc  │       │
│  │  Fees: 2% per txn       │         │  Fees: 2.9% + 30¢      │       │
│  └─────────────────────────┘         └─────────────────────────┘       │
└──────────────────────────────────────────────────────────────────────────┘
               │                                   │
               │                                   │
               ▼                                   ▼
        CUSTOMER BANK                      CUSTOMER BANK
        (Payment processed)                (Payment processed)


┌──────────────────────────────────────────────────────────────────────────┐
│                      ADDITIONAL SERVICES                                 │
│                                                                          │
│  ┌─────────────────────────┐         ┌─────────────────────────┐       │
│  │   EMAIL (Gmail SMTP)    │         │   MONITORING & LOGS     │       │
│  │                         │         │                         │       │
│  │  • Order confirmations  │         │  • Railway Dashboard    │       │
│  │  • Password resets      │         │  • Error tracking       │       │
│  │  • Shipping updates     │         │  • Performance metrics  │       │
│  │  • Marketing emails     │         │  • API usage stats      │       │
│  └─────────────────────────┘         └─────────────────────────┘       │
└──────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                           DATA FLOW EXAMPLE
═══════════════════════════════════════════════════════════════════════════

USER CHECKOUT FLOW:
──────────────────

1. User browses products on ashwathas.com (Vercel)
                ↓
2. Clicks "Add to Cart" → API call to api.ashwathas.com/cart/items
                ↓
3. Backend validates & saves to database (Supabase)
                ↓
4. User clicks "Checkout" → Creates order
                ↓
5. User selects payment method (Razorpay/Stripe)
                ↓
6. Frontend initiates payment → Payment gateway opens
                ↓
7. User completes payment → Gateway sends callback
                ↓
8. Backend verifies signature → Updates order status
                ↓
9. Send confirmation email (Gmail SMTP)
                ↓
10. User receives order confirmation & tracking


═══════════════════════════════════════════════════════════════════════════
                         SECURITY LAYERS
═══════════════════════════════════════════════════════════════════════════

1. HTTPS/SSL  →  All traffic encrypted (Auto by Vercel/Railway)
2. JWT Tokens  →  Secure authentication
3. Password Hashing  →  Bcrypt encryption
4. CORS Protection  →  Only allowed origins
5. Payment Signatures  →  Verified by backend
6. Input Validation  →  Pydantic schemas
7. SQL Injection Protection  →  SQLAlchemy ORM
8. Environment Variables  →  Secrets hidden
9. Rate Limiting  →  Prevent abuse (optional)


═══════════════════════════════════════════════════════════════════════════
                         SCALABILITY
═══════════════════════════════════════════════════════════════════════════

FREE TIER (0-1000 users/month):
  ✓ Vercel: Unlimited bandwidth
  ✓ Railway: 500 hours/month
  ✓ Supabase: 500MB storage
  ✓ Cost: ~₹100-200/month (domain only)

GROWING (1000-10000 users/month):
  ↑ Railway: Scale to $20/month
  ↑ Supabase: Upgrade to Pro ($25/month)
  ✓ Vercel: Still free
  ✓ Cost: ~₹4,000-5,000/month

ESTABLISHED (10000+ users/month):
  ↑ Railway: Multiple instances
  ↑ Supabase: Team plan
  ↑ CDN: Cloudflare Pro
  ✓ Cost: ~₹15,000-30,000/month


═══════════════════════════════════════════════════════════════════════════
                         DEVELOPMENT WORKFLOW
═══════════════════════════════════════════════════════════════════════════

LOCAL DEVELOPMENT:
  Your Computer → Git → GitHub → Deploy

CODE → TEST → COMMIT → PUSH → AUTO-DEPLOY

1. Code on your computer
2. Test locally (localhost:8000)
3. Git commit & push to GitHub
4. Railway auto-deploys backend
5. Vercel auto-deploys frontend
6. Live in ~2 minutes!


═══════════════════════════════════════════════════════════════════════════
```

This is your complete ASHWATHAS e-commerce system architecture!
