from fastapi import FastAPI, HTTPException, Query
from services.product_aggregtor import get_product_full_details
from services.product_services import get_all_platform_products
from services.master_products import (
    get_all_categories,
    get_products_by_category,
    search_products
)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Shop Pulse API running 🚀"}


@app.get("/categories")
def fetch_categories():
    categories = get_all_categories()

    return {
        "count": len(categories),
        "categories": categories
    }


@app.get("/products")
def get_products_by_cat(
    category: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        data = get_products_by_category(category, page, limit)

        if not data:
            raise HTTPException(status_code=404, detail="No products found")

        return {
            "category": category,
            "page": page,
            "limit": limit,
            "count": len(data),
            "products": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
def search(
    query: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        data = search_products(query, page, limit)

        return {
            "query": query,
            "page": page,
            "limit": limit,
            "count": len(data),
            "results": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{master_product_id}")
def get_product_details(master_product_id: str):
    try:
        data = get_product_full_details(master_product_id)

        if not data:
            raise HTTPException(status_code=404, detail="Product not found")

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/platformproducts")
def get_platform_products(
    platform: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query(None)
):
    try:
        data = get_all_platform_products(platform, page, limit, sort)

        return {
            "platform": platform,
            "page": page,
            "limit": limit,
            "count": len(data),
            "products": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))