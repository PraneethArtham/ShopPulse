"""
backend/services/local_store_service.py

Actual DB columns:
  local_stores         → store_id, store_name, location, phone, store_rating, created_at
  local_store_products → local_product_id, master_product_id, store_id,
                          product_name, price, stock_quantity, created_at
"""

import uuid
from typing import Optional
from backend.dbase.supabase_client import supabase


def get_local_stores(search: Optional[str] = None) -> list:
    # BUG FIX: filter on 'location' not 'city' (no city column)
    query = supabase.table("local_stores").select("*")
    if search:
        query = query.ilike("location", f"%{search}%")
    return query.execute().data or []


def create_local_store(
    store_name: str,
    location: str,
    phone: Optional[str] = None,
    store_rating: Optional[float] = None,
) -> dict:
    # BUG FIX: use 'location' column; removed address/city/latitude/longitude (don't exist)
    data = {
        "store_id": str(uuid.uuid4()),
        "store_name": store_name,
        "location": location,
        "phone": phone,
        "store_rating": store_rating,
    }
    supabase.table("local_stores").insert(data).execute()
    return data


def add_local_store_product(
    master_product_id: str,
    store_id: str,
    product_name: str,
    price: float,
    stock_quantity: int = 0,
) -> dict:
    # BUG FIX: use 'stock_quantity' not 'in_stock'/'notes' (don't exist)
    data = {
        "local_product_id": str(uuid.uuid4()),
        "master_product_id": master_product_id,
        "store_id": store_id,
        "product_name": product_name,
        "price": price,
        "stock_quantity": stock_quantity,
    }
    supabase.table("local_store_products").insert(data).execute()
    return data


def get_local_products_for_master(master_product_id: str) -> list:
    items = (
        supabase.table("local_store_products")
        .select("*")
        .eq("master_product_id", master_product_id)
        .execute()
        .data or []
    )
    result = []
    for item in items:
        # BUG FIX: safe limit(1) instead of .single()
        try:
            store_res = (
                supabase.table("local_stores")
                .select("*")
                .eq("store_id", item["store_id"])
                .limit(1)
                .execute()
            )
            item["store"] = store_res.data[0] if store_res.data else None
        except Exception:
            item["store"] = None

        # Derive in_stock from stock_quantity for frontend convenience
        qty = item.get("stock_quantity")
        item["in_stock"] = bool(qty and qty > 0)
        result.append(item)
    return result
