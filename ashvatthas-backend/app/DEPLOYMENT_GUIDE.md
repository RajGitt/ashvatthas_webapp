# 🌍 ASHWATHAS - Complete Deployment Guide
## From Code to Live Website - Step by Step

This guide will take you from having code files to a fully functional live website that anyone can access on the internet.

---

## 📋 PHASE 1: PREREQUISITES (What You Need)

### 1. Domain Name
- **Buy a domain** (e.g., ashwathas.com)
- **Where to buy:** 
  - GoDaddy (https://www.godaddy.com)
  - Namecheap (https://www.namecheap.com)
  - Google Domains (https://domains.google)
- **Cost:** ₹500-2000/year (~$8-25/year)

### 2. Hosting Service (Choose ONE)
**Option A: Simple & Beginner-Friendly**
- **Vercel** (Frontend) + **Railway** (Backend) - FREE to start
- **Netlify** (Frontend) + **Render** (Backend) - FREE to start

**Option B: More Control**
- **DigitalOcean** - $5-10/month
- **AWS** - Pay as you go
- **Heroku** - $7/month

**RECOMMENDED FOR BEGINNERS:** Vercel + Railway (Free tier!)

### 3. Database Hosting
- **Supabase** - FREE (Easiest, includes PostgreSQL)
- **Railway** - FREE tier included
- **ElephantSQL** - FREE tier
- **Neon** - FREE serverless PostgreSQL

**RECOMMENDED:** Supabase (Free + Easy)

### 4. Payment Gateway Accounts
- **Razorpay** (India) - Sign up at https://razorpay.com
- **Stripe** (International) - Sign up at https://stripe.com

---

## 🚀 PHASE 2: STEP-BY-STEP DEPLOYMENT

### Step 1: Setup Version Control (GitHub)

```bash
# 1. Install Git (if not installed)
# Windows: Download from https://git-scm.com/download/win
# Mac: brew install git
# Linux: sudo apt-get install git

# 2. Create a GitHub account at https://github.com

# 3. Create a new repository
# - Go to github.com
# - Click "New repository"
# - Name it "ashwathas-backend"
# - Make it private (for security)
# - Click "Create repository"

# 4. Initialize your project
cd /path/to/your/backend
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ashwathas-backend.git
git push -u origin main
```

### Step 2: Setup Database (Supabase - FREE)

1. **Go to https://supabase.com**
2. **Sign up** with GitHub
3. **Create a new project**
   - Project name: ashwathas-db
   - Database password: (choose strong password)
   - Region: Choose closest to India (e.g., Mumbai/Singapore)
   - Click "Create new project"

4. **Get your database URL**
   - Go to Settings → Database
   - Copy "Connection string" (URI format)
   - It looks like: `postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres`
   - **Save this!** You'll need it

5. **Convert to async format** (for FastAPI)
   ```
   Change: postgresql://...
   To:     postgresql+asyncpg://...
   ```

### Step 3: Setup Backend Hosting (Railway - FREE)

1. **Go to https://railway.app**
2. **Sign in with GitHub**
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select your repository** (ashwathas-backend)

5. **Add Environment Variables**
   - Click on your deployment
   - Go to "Variables" tab
   - Add these one by one:

   ```
   DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres
   SECRET_KEY=generate-a-32-char-random-string-here
   DEBUG=False
   ALLOWED_ORIGINS=https://yourfrontend.vercel.app
   
   # Razorpay
   RAZORPAY_KEY_ID=rzp_test_xxxxx
   RAZORPAY_KEY_SECRET=xxxxx
   
   # Stripe
   STRIPE_PUBLIC_KEY=pk_test_xxxxx
   STRIPE_SECRET_KEY=sk_test_xxxxx
   STRIPE_WEBHOOK_SECRET=whsec_xxxxx
   
   # Email (use Gmail)
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_FROM=noreply@ashwathas.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   ```

6. **Generate SECRET_KEY**
   ```python
   # Run this in Python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

7. **Add Start Command** (if not auto-detected)
   - Settings → Deploy
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

8. **Deploy!**
   - Railway will automatically deploy
   - You'll get a URL like: `https://ashwathas-backend-production.up.railway.app`
   - **Save this URL!**

### Step 4: Run Database Migrations

Railway automatically runs your app, but you need to create tables:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Connect to your project**
   ```bash
   railway link
   # Select your project
   ```

3. **Run migrations**
   ```bash
   railway run alembic upgrade head
   ```

### Step 5: Setup Frontend Hosting (Vercel - FREE)

1. **Update Frontend with Backend URL**
   - Open `ashwathas.html`
   - Add this JavaScript at the end (before `</script>`):

   ```javascript
   // API Configuration
   const API_BASE_URL = 'https://YOUR-RAILWAY-URL.up.railway.app/api/v1';
   
   // Example: Add to cart function
   async function addToCart(productVariantId, quantity) {
       const token = localStorage.getItem('access_token');
       
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
       
       return await response.json();
   }
   
   // Login function
   async function login(email, password) {
       const response = await fetch(`${API_BASE_URL}/auth/login`, {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json'
           },
           body: JSON.stringify({ email, password })
       });
       
       const data = await response.json();
       localStorage.setItem('access_token', data.access_token);
       return data;
   }
   ```

2. **Go to https://vercel.com**
3. **Sign in with GitHub**
4. **Create New Project**
   - Import your repository OR upload files directly
   - If uploading directly:
     - Create a new folder with your HTML file
     - Rename it to `index.html`
     - Drag and drop to Vercel

5. **Deploy!**
   - Vercel will give you a URL like: `https://ashwathas.vercel.app`
   - **This is your live website!**

### Step 6: Connect Your Domain

#### For Vercel (Frontend):
1. Go to your project → Settings → Domains
2. Add your domain: `ashwathas.com`
3. Follow instructions to update DNS records at your domain registrar

#### For Railway (Backend):
1. Go to Settings → Domains
2. Add custom domain: `api.ashwathas.com`
3. Update DNS records at your domain registrar

**DNS Records to Add:**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: A
Name: @
Value: 76.76.21.21 (Vercel IP)

Type: CNAME
Name: api
Value: YOUR-APP.up.railway.app
```

### Step 7: Setup Payment Gateways

#### Razorpay (for Indian payments):

1. **Sign up at https://razorpay.com**
2. **Verify your business**
   - Submit business documents
   - Bank account details
   - PAN/GST details
3. **Get Test Keys** (for testing)
   - Dashboard → Settings → API Keys
   - Generate Test Key
   - Copy Key ID and Key Secret
4. **Add to Railway environment variables**
5. **Go Live**
   - Once tested, submit for activation
   - After approval, generate Live Keys
   - Replace test keys with live keys

#### Stripe (for international):

1. **Sign up at https://stripe.com**
2. **Get Test Keys**
   - Dashboard → Developers → API Keys
   - Copy Publishable and Secret keys
3. **Add to Railway environment variables**
4. **Activate Account**
   - Complete business verification
   - Add bank account
5. **Go Live**
   - Switch to Live mode in dashboard
   - Get Live keys
   - Replace test keys with live keys

### Step 8: Setup Email (Gmail for notifications)

1. **Enable 2-Factor Authentication** on your Gmail
2. **Create App Password**
   - Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Name it "ASHWATHAS"
   - Copy the 16-character password
3. **Add to Railway environment variables**
   ```
   MAIL_USERNAME=youremail@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

---

## 🧪 PHASE 3: TESTING

### Test Your Live Website:

1. **Frontend Test**
   ```
   Visit: https://ashwathas.vercel.app
   - Should see your beautiful website
   - Check all sections load
   - Check responsive design on mobile
   ```

2. **Backend Test**
   ```
   Visit: https://your-railway-url.up.railway.app/api/docs
   - Should see API documentation
   - Try the "Try it out" buttons
   ```

3. **Full Flow Test**
   - Register a new user
   - Login
   - Add items to cart
   - Create an order
   - Make a test payment (use test cards)

---

## 📊 PHASE 4: MONITORING & MAINTENANCE

### 1. Setup Analytics
- **Google Analytics** - Free
  - Sign up at https://analytics.google.com
  - Add tracking code to your HTML

### 2. Monitor Backend
- **Railway Dashboard** - Shows logs, errors, usage
- **Sentry** - Free error tracking (optional)
  - https://sentry.io

### 3. Backup Database
- **Supabase** - Automatic backups (check settings)
- Set up weekly manual backups

### 4. SSL/HTTPS
- **Vercel** - Automatic SSL ✅
- **Railway** - Automatic SSL ✅
- **Custom domain** - SSL auto-provisioned

---

## 💰 MONTHLY COSTS (Estimate)

**Starting Out (FREE Tier):**
- Frontend (Vercel): **FREE**
- Backend (Railway): **FREE** (500 hours/month)
- Database (Supabase): **FREE** (500MB)
- Domain: **₹100-200/month** (~$1.50-2.50)
- **TOTAL: ~₹100-200/month** to start!

**Growing Business:**
- Frontend (Vercel Pro): **$20/month**
- Backend (Railway): **$5-20/month**
- Database (Supabase Pro): **$25/month**
- Domain: **₹100-200/month**
- Payment Gateway: **2-3% per transaction**
- **TOTAL: ~₹4,000-5,000/month** (~$50-60)

---

## 🆘 COMMON ISSUES & SOLUTIONS

### Issue 1: "502 Bad Gateway"
**Solution:** Backend not running
- Check Railway logs
- Check environment variables
- Ensure database is accessible

### Issue 2: CORS Errors
**Solution:** 
```python
# In Railway environment variables, add:
ALLOWED_ORIGINS=https://ashwathas.vercel.app,https://www.ashwathas.com
```

### Issue 3: Database Connection Failed
**Solution:**
- Check DATABASE_URL format (must be `postgresql+asyncpg://...`)
- Check Supabase database is running
- Check IP allowlist (Supabase Settings → Database → Connection pooling)

### Issue 4: Payments Not Working
**Solution:**
- Verify you're using test keys in test mode
- Check webhook URLs are configured
- For Razorpay: Dashboard → Webhooks → Add webhook URL
- For Stripe: Dashboard → Webhooks → Add endpoint

### Issue 5: Emails Not Sending
**Solution:**
- Verify Gmail app password is correct
- Check 2FA is enabled
- Try "Less secure app access" (not recommended)

---

## 🎯 QUICK START CHECKLIST

- [ ] Buy domain name
- [ ] Create GitHub account & repository
- [ ] Create Supabase account & database
- [ ] Create Railway account & deploy backend
- [ ] Add all environment variables to Railway
- [ ] Run database migrations
- [ ] Create Vercel account & deploy frontend
- [ ] Update frontend with backend URL
- [ ] Connect custom domain
- [ ] Sign up for Razorpay & Stripe
- [ ] Get test API keys
- [ ] Test the entire flow
- [ ] Set up Gmail for emails
- [ ] Go live with payment gateways
- [ ] Add SSL certificates
- [ ] Setup monitoring

---

## 📞 SUPPORT RESOURCES

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Razorpay Docs:** https://razorpay.com/docs
- **Stripe Docs:** https://stripe.com/docs

---

## 🚀 YOU'RE READY TO LAUNCH!

Follow these steps in order, and within a few hours, ASHWATHAS will be live on the internet! 

**Remember:**
1. Start with FREE tiers to test everything
2. Use TEST mode for payments initially
3. Only go LIVE after thorough testing
4. Monitor your logs regularly
5. Keep your API keys SECRET (never commit to GitHub)

**Good luck! 🌿**

---

**Need help?** Each platform has excellent documentation and community support. Don't hesitate to check their docs or ask in their Discord/community channels.
