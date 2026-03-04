"""
backend/services/product_services.py
Handles platform product CRUD operations.
"""

import uuid
from typing import Optional
from backend.dbase.supabase_client import supabase
from backend.services.master_products import get_or_create_master_product


def insert_platform_product(
    product_name: str,
    price: float,
    platform_name: str,
    seller_id: Optional[str] = None,
    rating: Optional[float] = None,
    product_url: Optional[str] = None,
    image_url: Optional[str] = None,
    category: str = "General",
) -> dict:
    master_product_id = get_or_create_master_product(product_name, category=category)
    data = {
        "platform_product_id": str(uuid.uuid4()),
        "master_product_id": master_product_id,
        "seller_id": seller_id,
        "platform_name": platform_name,
        "product_name": product_name,
        "price": price,
        "rating": rating,
        "product_url": product_url,
        "image_url": image_url,
    }
    supabase.table("platform_products").insert(data).execute()
    return data


def delete_platform_product(platform_product_id: str) -> dict:
    return (
        supabase.table("platform_products")
        .delete()
        .eq("platform_product_id", platform_product_id)
        .execute()
    )


def get_all_platform_products(
    platform: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort: Optional[str] = None,
) -> list:
    query = supabase.table("platform_products").select("*")
    if platform:
        query = query.eq("platform_name", platform)
    if sort == "price_asc":
        query = query.order("price", desc=False)
    elif sort == "price_desc":
        query = query.order("price", desc=True)
    start = (page - 1) * limit
    query = query.range(start, start + limit - 1)
    return query.execute().data
