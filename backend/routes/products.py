"""
backend/routes/products.py
Routes for master products, search, categories, and price comparison.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.services.master_products import (
    get_all_categories,
    get_products_by_category,
    search_products,
)
from backend.services.product_aggregator import get_product_full_details

router = APIRouter(tags=["Products"])


@router.get("/categories")
def fetch_categories():
    categories = get_all_categories()
    return {"count": len(categories), "categories": categories}


@router.get("/products")
def get_products_by_cat(
    category: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    try:
        data = get_products_by_category(category, page, limit, sort)
        if not data:
            raise HTTPException(status_code=404, detail="No products found")
        return {"category": category, "page": page, "limit": limit, "count": len(data), "products": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{master_product_id}")
def get_product_details(master_product_id: str):
    try:
        data = get_product_full_details(master_product_id)
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    try:
        data = search_products(query, page, limit)
        return {"query": query, "page": page, "limit": limit, "count": len(data), "results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/{master_product_id}")
def compare_prices(master_product_id: str):
    """Sorted price comparison across all platforms + local stores."""
    try:
        data = get_product_full_details(master_product_id)
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")

        online = [
            {
                "source": item["platform_name"],
                "type": "online",
                "price": item["price"],
                "rating": item.get("rating"),
                "url": item.get("product_url"),
                "seller": item.get("seller", {}).get("seller_name") if item.get("seller") else None,
            }
            for item in data["platform_listings"]
        ]
        local = [
            {
                "source": item["store"]["store_name"],
                "type": "local",
                "price": item["price"],
                "in_stock": item.get("in_stock"),
                "address": item["store"].get("address"),
            }
            for item in data["local_store_listings"]
            if item.get("store")
        ]

        all_options = sorted(online + local, key=lambda x: x["price"] or float("inf"))
        return {
            "product": data["product"],
            "best_deal": all_options[0] if all_options else None,
            "all_options": all_options,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
