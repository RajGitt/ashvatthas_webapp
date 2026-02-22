# Import all models so Alembic can find them
from app.models.user import User, Address
from app.models.product import Product, ProductVariant
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.payment import Payment, PaymentMethod, PaymentGateway

__all__ = [
    "User",
    "Address",
    "Product",
    "ProductVariant",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "OrderStatus",
    "PaymentStatus",
    "Payment",
    "PaymentMethod",
    "PaymentGateway",
]



"""
## 🎯 **What This Does:**

This file tells Python and Alembic:
- "Here are all the database models (tables) in this folder"
- Imports them so Alembic can automatically detect them
- Makes them available when you write `from app.models import User`

---

## ✅ **Step-by-Step:**

1. **Open** `app/models/__init__.py` in VS Code
2. **Delete** everything that's currently in it (if anything)
3. **Paste** the code above
4. **Save** the file (Ctrl+S or Cmd+S)

---

## 📋 **Final Check:**

Your `app/models/` folder should now have:
```
app/models/
├── __init__.py      ← Contains the imports above
├── user.py          ← User & Address models
├── product.py       ← Product & ProductVariant models
├── cart.py          ← Cart & CartItem models
├── order.py         ← Order & OrderItem models
└── payment.py       ← Payment model
"""

