# 🏠 ASHWATHAS - LOCAL TESTING GUIDE
## See Your Website Working on Your Computer (No Hosting Needed!)

This guide will help you run ASHWATHAS on your own computer so you can show your friend how it looks and works - NO payment, NO domain needed yet!

---

## 📋 WHAT YOU NEED ON YOUR COMPUTER

### Required Software (All FREE):

1. **Python 3.10+** 
   - Download: https://www.python.org/downloads/
   - ✅ During installation: CHECK "Add Python to PATH"

2. **PostgreSQL Database**
   - Download: https://www.postgresql.org/download/
   - ✅ Remember the password you set during installation

3. **VS Code** (Code Editor - Optional but recommended)
   - Download: https://code.visualstudio.com/

4. **Web Browser** (Chrome/Firefox/Edge - you already have this)

---

## 🚀 PART 1: SETUP BACKEND (30 minutes)

### Step 1: Create Project Folder

```bash
# Open Terminal/Command Prompt

# Windows:
cd C:\Users\YourName\Desktop
mkdir ashwathas-project
cd ashwathas-project

# Mac/Linux:
cd ~/Desktop
mkdir ashwathas-project
cd ashwathas-project
```

### Step 2: Copy Your Backend Files

```bash
# Copy all the backend files I gave you into this folder
# Your folder should look like:
ashwathas-project/
├── app/
├── requirements.txt
├── .env.example
├── README.md
└── QUICKSTART.md
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Your terminal should now show (venv) at the start
```

### Step 4: Install Dependencies

```bash
# This will install all required packages
pip install -r requirements.txt

# Wait 2-3 minutes for installation to complete
```

### Step 5: Setup Database

```bash
# Open PostgreSQL command line (pgAdmin or psql)
# Create database

# Option A: Using pgAdmin (GUI)
# 1. Open pgAdmin
# 2. Right-click on "Databases"
# 3. Create → Database
# 4. Name: ashwathas_db
# 5. Click Save

# Option B: Using psql command line
psql -U postgres
CREATE DATABASE ashwathas_db;
\q
```

### Step 6: Create Environment File

```bash
# Copy the example file
# Windows:
copy .env.example .env

# Mac/Linux:
cp .env.example .env

# Now edit .env file with these values:
```

**Edit `.env` file (use Notepad/VS Code):**

```env
# Application
APP_NAME=ASHWATHAS
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-to-anything-random-32chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database - UPDATE THIS with your PostgreSQL password
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/ashwathas_db

# Email - Use fake values for now
MAIL_USERNAME=test@gmail.com
MAIL_PASSWORD=fakepassword
MAIL_FROM=noreply@ashwathas.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Payment - Use DEMO/FAKE keys for now (we'll skip payment testing)
RAZORPAY_KEY_ID=demo_key
RAZORPAY_KEY_SECRET=demo_secret
STRIPE_PUBLIC_KEY=demo_public
STRIPE_SECRET_KEY=demo_secret
STRIPE_WEBHOOK_SECRET=demo_webhook

# Frontend
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:8000
```

**IMPORTANT:** Change `YOUR_POSTGRES_PASSWORD` to the password you set when installing PostgreSQL!

### Step 7: Create Database Tables

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial tables"

# Apply migration (create tables)
alembic upgrade head

# You should see: "Running upgrade -> xxxxx, Initial tables"
```

### Step 8: Start Backend Server

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

**🎉 BACKEND IS RUNNING!**

Test it: Open browser and go to:
- **http://127.0.0.1:8000** - Should show welcome message
- **http://127.0.0.1:8000/api/docs** - Should show API documentation (Swagger UI)

**KEEP THIS TERMINAL OPEN!** Backend is running here.

---

## 🎨 PART 2: SETUP FRONTEND (5 minutes)

### Step 1: Update Frontend with Local Backend URL

Open `ashwathas.html` in a text editor and add this JavaScript code at the **very end**, just before `</body>`:

```html
    <!-- ... existing content ... -->
    
    <script>
        // ============================================
        // BACKEND API INTEGRATION
        // ============================================
        
        const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
        
        // ============================================
        // AUTH FUNCTIONS
        // ============================================
        
        async function registerUser(email, username, password, fullName) {
            try {
                const response = await fetch(`${API_BASE_URL}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        username: username,
                        password: password,
                        full_name: fullName
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Registration failed');
                }
                
                const data = await response.json();
                alert('Registration successful! Please login.');
                return data;
            } catch (error) {
                alert('Error: ' + error.message);
                console.error('Registration error:', error);
            }
        }
        
        async function loginUser(email, password) {
            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Login failed');
                }
                
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user_email', email);
                alert('Login successful!');
                updateUIAfterLogin();
                return data;
            } catch (error) {
                alert('Error: ' + error.message);
                console.error('Login error:', error);
            }
        }
        
        function logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_email');
            alert('Logged out successfully');
            updateUIAfterLogout();
        }
        
        function getAuthToken() {
            return localStorage.getItem('access_token');
        }
        
        function isLoggedIn() {
            return !!getAuthToken();
        }
        
        // ============================================
        // CART FUNCTIONS
        // ============================================
        
        async function getCart() {
            try {
                const token = getAuthToken();
                if (!token) {
                    alert('Please login first');
                    return;
                }
                
                const response = await fetch(`${API_BASE_URL}/cart/`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (!response.ok) throw new Error('Failed to get cart');
                
                const cart = await response.json();
                console.log('Cart:', cart);
                displayCart(cart);
                return cart;
            } catch (error) {
                console.error('Get cart error:', error);
            }
        }
        
        async function addToCart(productVariantId, quantity = 1) {
            try {
                const token = getAuthToken();
                if (!token) {
                    alert('Please login first');
                    return;
                }
                
                const response = await fetch(`${API_BASE_URL}/cart/items`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        product_variant_id: productVariantId,
                        quantity: quantity
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to add to cart');
                }
                
                alert('Added to cart!');
                getCart(); // Refresh cart display
            } catch (error) {
                alert('Error: ' + error.message);
                console.error('Add to cart error:', error);
            }
        }
        
        function displayCart(cart) {
            console.log('=== YOUR CART ===');
            console.log('Total items:', cart.total_items);
            console.log('Total price: ₹' + cart.total_price);
            console.log('Items:', cart.items);
            console.log('================');
        }
        
        // ============================================
        // UI UPDATE FUNCTIONS
        // ============================================
        
        function updateUIAfterLogin() {
            const email = localStorage.getItem('user_email');
            console.log('Logged in as:', email);
            // You can update UI here to show user is logged in
        }
        
        function updateUIAfterLogout() {
            console.log('Logged out');
            // You can update UI here to show user is logged out
        }
        
        // ============================================
        // DEMO FUNCTIONS - Open browser console to test!
        // ============================================
        
        console.log('=================================');
        console.log('ASHWATHAS API Demo');
        console.log('=================================');
        console.log('Open browser console (F12) and try:');
        console.log('');
        console.log('1. Register:');
        console.log('   registerUser("test@email.com", "testuser", "password123", "Test User")');
        console.log('');
        console.log('2. Login:');
        console.log('   loginUser("test@email.com", "password123")');
        console.log('');
        console.log('3. Get Cart:');
        console.log('   getCart()');
        console.log('');
        console.log('4. Logout:');
        console.log('   logout()');
        console.log('=================================');
        
        // Check if user is already logged in
        if (isLoggedIn()) {
            console.log('Already logged in!');
            updateUIAfterLogin();
        }
    </script>
</body>
</html>
```

### Step 2: Open Frontend in Browser

**Simple way:**
1. Just **double-click** `ashwathas.html` file
2. It will open in your default browser

**OR open with live server (better):**
```bash
# Install a simple HTTP server
npm install -g http-server

# OR if you don't have npm, use Python:
python -m http.server 3000

# Then open: http://localhost:3000/ashwathas.html
```

**🎉 FRONTEND IS RUNNING!**

---

## 🧪 PART 3: TEST EVERYTHING (15 minutes)

### Visual Testing:

1. **Open your website:** Double-click `ashwathas.html`
   - You should see your beautiful ASHWATHAS website
   - Scroll through all sections
   - Check the colors, fonts, layout
   - **Show this to your friend!** ✨

### Functionality Testing:

1. **Open Browser Console** (Press F12 or Right-click → Inspect → Console tab)

2. **Register a new user:**
   ```javascript
   registerUser("john@email.com", "john123", "securepass", "John Doe")
   ```
   - Should show "Registration successful!"

3. **Login:**
   ```javascript
   loginUser("john@email.com", "securepass")
   ```
   - Should show "Login successful!"

4. **Check your cart:**
   ```javascript
   getCart()
   ```
   - Should show your cart details in console

5. **Logout:**
   ```javascript
   logout()
   ```

### View API Documentation:

Go to: **http://127.0.0.1:8000/api/docs**

You'll see a beautiful interactive API documentation (Swagger UI) where you can:
- See all available endpoints
- Test API calls directly
- See request/response formats

**Try this:**
1. Click on `POST /api/v1/auth/register`
2. Click "Try it out"
3. Fill in the form
4. Click "Execute"
5. See the response!

---

## 🎬 DEMO FOR YOUR FRIEND

### What to Show:

1. **The Beautiful Website**
   - Open `ashwathas.html` in full screen
   - Show the elegant design, colors, animations
   - Show mobile responsive (press F12 → click phone icon)

2. **The Working Backend**
   - Show `http://127.0.0.1:8000/api/docs`
   - Show all the APIs you built
   - Demonstrate a live API call

3. **The Database**
   - Open pgAdmin
   - Show the tables you created
   - Show actual user data stored

4. **Live Demo:**
   ```
   "Watch this - I can register a user right now!"
   → Open console
   → Run: registerUser("demo@test.com", "demo", "pass123", "Demo User")
   → Show success message
   → Open pgAdmin
   → Refresh users table
   → "See? The user is in the database!"
   ```

---

## 📸 WHAT EACH PART LOOKS LIKE

### 1. Website (ashwathas.html):
```
┌─────────────────────────────────────────┐
│  ASHWATHAS                         Menu │
├─────────────────────────────────────────┤
│                                         │
│           ASHWATHAS                     │
│        Contemporary Living              │
│                                         │
│              [Scroll]                   │
├─────────────────────────────────────────┤
│      Curated Collections                │
│   [Essence] [Verdant] [Serenity]       │
├─────────────────────────────────────────┤
│         Our Philosophy                  │
│    "Beautiful text about design..."     │
└─────────────────────────────────────────┘
```

### 2. API Docs (http://127.0.0.1:8000/api/docs):
```
┌─────────────────────────────────────────┐
│  ASHWATHAS API Documentation            │
├─────────────────────────────────────────┤
│  Authentication                         │
│    POST /api/v1/auth/register  ▼        │
│    POST /api/v1/auth/login     ▼        │
│                                         │
│  Shopping Cart                          │
│    GET  /api/v1/cart/          ▼        │
│    POST /api/v1/cart/items     ▼        │
│                                         │
│  Payments                               │
│    POST /api/v1/payments/create ▼       │
└─────────────────────────────────────────┘
```

### 3. Database (pgAdmin):
```
┌─────────────────────────────────────────┐
│  ashwathas_db                           │
├─────────────────────────────────────────┤
│  Tables:                                │
│    ▼ users                              │
│    ▼ addresses                          │
│    ▼ products                           │
│    ▼ carts                              │
│    ▼ orders                             │
│    ▼ payments                           │
└─────────────────────────────────────────┘
```

---

## ⚡ QUICK TROUBLESHOOTING

### Problem: "Module not found" error
**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Install again
pip install -r requirements.txt
```

### Problem: Database connection error
**Solution:**
```bash
# Check PostgreSQL is running
# Windows: Open Services → PostgreSQL should be "Running"
# Mac: brew services list
# Linux: sudo service postgresql status

# Check your .env file has correct password
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/ashwathas_db
```

### Problem: "Address already in use" (Port 8000)
**Solution:**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001

# Update frontend API_BASE_URL to: http://127.0.0.1:8001/api/v1
```

### Problem: CORS error in browser
**Solution:**
```bash
# Make sure backend is running
# Check .env has:
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:8000,http://localhost:8080
```

---

## ✅ CHECKLIST

- [ ] Python installed (check: `python --version`)
- [ ] PostgreSQL installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (ashwathas_db)
- [ ] .env file created and configured
- [ ] Database tables created (`alembic upgrade head`)
- [ ] Backend running (`uvicorn app.main:app --reload`)
- [ ] Frontend opened in browser
- [ ] Can see the website
- [ ] Can register a user
- [ ] Can login
- [ ] API docs accessible

---

## 🎯 NEXT STEPS (After showing your friend)

Once your friend is impressed and you're ready to go live:

1. **Buy domain name** (~₹500-2000/year)
2. **Sign up for hosting** (Vercel, Railway, Supabase - all FREE to start)
3. **Deploy using DEPLOYMENT_GUIDE.md**
4. **Go live in 2-3 hours!**

---

## 💡 PRO TIPS

1. **Take Screenshots** of your working system to show people
2. **Record a Video** using OBS or screen recording
3. **Create Sample Products** to make it look real
4. **Test on mobile** - website is fully responsive
5. **Show the code** - it's clean and professional

---

**You now have a FULLY WORKING e-commerce system on your computer! 🎉**

No internet needed, no hosting needed, no payment needed - everything runs locally and you can show your friend how professional and polished ASHWATHAS is!
