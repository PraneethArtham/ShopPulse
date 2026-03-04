# ShopPulse 🛍️

**India's smart price aggregator** — compare prices across Amazon, Flipkart, Meesho & local stores in one place.

---

## 📁 Project Structure

```
ShopPulse/
│
├── backend/                         # Python FastAPI backend
│   ├── dbase/
│   │   ├── __init__.py
│   │   └── supabase_client.py       # Supabase connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── products.py              # /categories, /products, /search, /compare
│   │   ├── platform_products.py     # /platformproducts CRUD
│   │   ├── local_stores.py          # /localstores, /localstoreproducts
│   │   ├── sellers.py               # /sellers CRUD
│   │   └── reviews.py               # /reviews CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   ├── master_products.py       # Master product logic
│   │   ├── product_services.py      # Platform product CRUD
│   │   ├── product_aggregator.py    # Full product detail aggregation
│   │   ├── seller_service.py        # Seller CRUD
│   │   ├── review_service.py        # Review CRUD
│   │   └── local_store_service.py   # Local store CRUD
│   └── __init__.py
│
├── frontend/                        # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/              # Shared UI components
│   │   │   ├── Navbar.jsx + .module.css
│   │   │   ├── ProductCard.jsx + .module.css
│   │   │   ├── Loader.jsx + .module.css
│   │   │   ├── Breadcrumb.jsx + .module.css
│   │   │   └── EmptyState.jsx + .module.css
│   │   ├── pages/                   # Route-level pages
│   │   │   ├── Home.jsx + .module.css
│   │   │   ├── Category.jsx + .module.css
│   │   │   ├── ProductDetails.jsx + .module.css
│   │   │   └── Search.jsx + .module.css
│   │   ├── hooks/
│   │   │   └── useFetch.js          # Generic data-fetching hook
│   │   ├── context/
│   │   │   └── CartContext.js       # Wishlist context
│   │   ├── utils/
│   │   │   ├── api.js               # Axios instance + typed helpers
│   │   │   └── helpers.js           # formatPrice, renderStars, etc.
│   │   ├── styles/
│   │   │   └── globals.css          # Design tokens + global styles
│   │   ├── App.jsx                  # Router + providers
│   │   └── index.js                 # React entry point
│   └── package.json
│
├── main.py                          # FastAPI app entry point
├── scrapping.py                     # Multi-platform Selenium scraper
├── schema.sql                       # Supabase DB schema + seed data
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** → paste `schema.sql` → Run
3. Copy your **Project URL** and **service_role key** (Settings → API)

### 2. Backend

```bash
# Install Python deps
pip install -r requirements.txt

# Create .env from example
cp .env.example .env
# Edit .env and fill in SUPABASE_URL and SUPABASE_KEY

# Run the API
uvicorn main:app --reload --port 8000
```

API docs: **http://localhost:8000/docs**

### 3. Frontend

```bash
cd frontend
npm install
npm start
```

App runs at: **http://localhost:3000**

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/categories` | All product categories |
| GET | `/products?category=Electronics` | Products by category (+ sort, pagination) |
| GET | `/products/{id}` | Full product with all platform + local store data |
| GET | `/search?query=iphone` | Search by name or brand |
| GET | `/compare/{id}` | Sorted price comparison (best deal highlighted) |
| GET/POST | `/platformproducts` | List or create platform listings |
| DELETE | `/platformproducts/{id}` | Remove a platform listing |
| GET | `/localstores` | All local stores (filter by city) |
| POST | `/localstores` | Add a local store |
| GET/POST | `/localstoreproducts` | Local store inventory |
| GET/POST | `/sellers` | Seller management |
| POST | `/reviews` | Add a review |
| GET | `/reviews/product/{id}` | All reviews for a master product |

---

## 🕷️ Scraper

```bash
# Scrape all 3 platforms
python scrapping.py --query "sony headphones" --category "Electronics"

# Specific platforms only
python scrapping.py -q "iphone 15" -c "Mobiles" -p amazon flipkart

# Run without browser window
python scrapping.py -q "macbook" --headless

# Interactive mode
python scrapping.py
```

---

## 🗄️ Database Schema

```
master_products           ← canonical product registry
  ├── platform_products   ← Amazon / Flipkart / Meesho listings
  │     └── reviews       ← customer reviews per platform listing
  └── local_store_products← local store inventory
sellers                   ← seller profiles
local_stores              ← physical store info
```
