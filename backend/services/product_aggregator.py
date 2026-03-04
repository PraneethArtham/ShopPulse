"""
backend/services/product_aggregator.py
Aggregates full product details: master info + all platform listings
+ sellers + reviews + local store listings.

Actual DB schema:
  master_products      → master_product_id, product_name, brand, category, description, created_at
  platform_products    → platform_product_id, master_product_id, seller_id, platform_name,
                          price, rating, product_url, image_url, product_name, created_at
  sellers              → seller_id, seller_name, seller_rating, created_at
  reviews              → review_id, platform_product_id, review_text, review_rating,
                          sentiment_score, is_fake, created_at
  local_stores         → store_id, store_name, location, phone, store_rating, created_at
  local_store_products → local_product_id, master_product_id, store_id, product_name,
                          price, stock_quantity, created_at
"""

from backend.dbase.supabase_client import supabase


def _safe_fetch_one(table: str, col: str, val: str) -> dict | None:
    """Fetch one row safely — never raises, returns None if missing."""
    try:
        res = (
            supabase.table(table)
            .select("*")
            .eq(col, val)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None
    except Exception:
        return None


def get_product_full_details(master_product_id: str) -> dict | None:
    # ── 1. Master product ──────────────────────────────────────
    # BUG FIX: replaced .single().execute() with safe limit(1) fetch
    product = _safe_fetch_one("master_products", "master_product_id", master_product_id)
    if not product:
        return None

    # ── 2. Platform listings ───────────────────────────────────
    try:
        platforms_res = (
            supabase.table("platform_products")
            .select("*")
            .eq("master_product_id", master_product_id)
            .execute()
        )
        platform_rows = platforms_res.data or []
    except Exception:
        platform_rows = []

    platform_data = []
    for item in platform_rows:
        # BUG FIX: sellers has no platform_name; safe fetch instead of .single()
        if item.get("seller_id"):
            item["seller"] = _safe_fetch_one("sellers", "seller_id", item["seller_id"])
        else:
            item["seller"] = None

        # BUG FIX: order by created_at (not "date" — that column doesn't exist)
        try:
            reviews_res = (
                supabase.table("reviews")
                .select("*")
                .eq("platform_product_id", item["platform_product_id"])
                .order("created_at", desc=True)
                .execute()
            )
            item["reviews"] = reviews_res.data or []
        except Exception:
            item["reviews"] = []

        platform_data.append(item)

    # Sort by price ascending
    platform_data.sort(key=lambda x: x.get("price") or float("inf"))

    # ── 3. Local store listings ────────────────────────────────
    try:
        local_res = (
            supabase.table("local_store_products")
            .select("*")
            .eq("master_product_id", master_product_id)
            .execute()
        )
        local_rows = local_res.data or []
    except Exception:
        local_rows = []

    local_data = []
    for item in local_rows:
        # BUG FIX: safe fetch instead of .single() which throws on 0 rows
        store = _safe_fetch_one("local_stores", "store_id", item["store_id"])
        item["store"] = store
        # BUG FIX: DB has stock_quantity (int), not in_stock (bool)
        qty = item.get("stock_quantity")
        item["in_stock"] = bool(qty and qty > 0)
        local_data.append(item)

    return {
        "product": product,
        "platform_listings": platform_data,
        "local_store_listings": local_data,
    }
