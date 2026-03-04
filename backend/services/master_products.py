"""
backend/services/master_products.py
Handles master product creation, search, and category queries.
"""

import uuid
from typing import Optional
from backend.dbase.supabase_client import supabase


def extract_brand(product_name: str) -> str:
    return product_name.split()[0]


def get_or_create_master_product(product_name: str, category: str = "General") -> str:
    result = (
        supabase.table("master_products")
        .select("*")
        .ilike("product_name", product_name)
        .execute()
    )
    if result.data:
        return result.data[0]["master_product_id"]

    new_product = {
        "master_product_id": str(uuid.uuid4()),
        "product_name": product_name,
        "brand": extract_brand(product_name),
        "category": category,
        "description": f"{product_name} — aggregated from multiple platforms.",
    }
    supabase.table("master_products").insert(new_product).execute()
    return new_product["master_product_id"]


def get_all_categories() -> list:
    response = supabase.table("master_products").select("category").execute()
    return sorted(list(set(
        item["category"] for item in response.data if item.get("category")
    )))


def get_products_by_category(
    category: str,
    page: int = 1,
    limit: int = 20,
    sort: Optional[str] = None,
) -> list:
    start = (page - 1) * limit
    end = start + limit - 1
    query = supabase.table("master_products").select("*").eq("category", category)
    if sort == "name_asc":
        query = query.order("product_name", desc=False)
    elif sort == "name_desc":
        query = query.order("product_name", desc=True)
    return query.range(start, end).execute().data


def search_products(query: str, page: int = 1, limit: int = 20) -> list:
    start = (page - 1) * limit
    end = start + limit - 1
    by_name = (
        supabase.table("master_products")
        .select("*")
        .ilike("product_name", f"%{query}%")
        .range(start, end)
        .execute()
        .data
    )
    by_brand = (
        supabase.table("master_products")
        .select("*")
        .ilike("brand", f"%{query}%")
        .range(start, end)
        .execute()
        .data
    )
    seen = set()
    merged = []
    for item in by_name + by_brand:
        if item["master_product_id"] not in seen:
            seen.add(item["master_product_id"])
            merged.append(item)
    return merged[:limit]
