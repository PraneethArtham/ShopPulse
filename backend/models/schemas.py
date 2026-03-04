"""
backend/models/schemas.py
Pydantic schemas matching the ACTUAL Supabase column names.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ── Master Product ─────────────────────────────────────────────
class MasterProductOut(BaseModel):
    master_product_id: str
    product_name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


# ── Seller  (sellers table: seller_id, seller_name, seller_rating) ──
class SellerIn(BaseModel):
    seller_name: str
    seller_rating: Optional[float] = None
    # BUG FIX: removed platform_name — that column does not exist on sellers table


# ── Platform Product ───────────────────────────────────────────
class PlatformProductIn(BaseModel):
    product_name: str
    price: float
    platform_name: str
    seller_id: Optional[str] = None
    rating: Optional[float] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    category: str = "General"


# ── Review  (actual columns: review_text, review_rating, sentiment_score, is_fake) ──
class ReviewIn(BaseModel):
    platform_product_id: str
    # BUG FIX: use real column names
    review_text: Optional[str] = None
    review_rating: float = Field(..., ge=1, le=5)
    sentiment_score: Optional[float] = None
    is_fake: bool = False


# ── Local Store  (actual columns: store_name, location, phone, store_rating) ──
class LocalStoreIn(BaseModel):
    store_name: str
    # BUG FIX: 'location' not 'address'/'city' — those columns don't exist
    location: str
    phone: Optional[str] = None
    store_rating: Optional[float] = None


# ── Local Store Product  (actual columns: product_name, price, stock_quantity) ──
class LocalStoreProductIn(BaseModel):
    master_product_id: str
    store_id: str
    product_name: str
    price: float
    # BUG FIX: stock_quantity (int) not in_stock (bool) + notes
    stock_quantity: int = 0
