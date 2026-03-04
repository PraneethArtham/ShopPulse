"""
main.py — ShopPulse API Entry Point
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import products, platform_products, local_stores, sellers, reviews

app = FastAPI(
    title="ShopPulse API",
    description="India's smart price aggregator — compare prices across Amazon, Flipkart, Meesho & local stores.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(products.router)
app.include_router(platform_products.router)
app.include_router(local_stores.router)
app.include_router(sellers.router)
app.include_router(reviews.router)


@app.get("/", tags=["Health"])
def health():
    return {"message": "ShopPulse API running 🚀", "version": "1.0.0", "docs": "/docs"}
