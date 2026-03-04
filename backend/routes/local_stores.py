"""
backend/routes/local_stores.py
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.models.schemas import LocalStoreIn, LocalStoreProductIn
from backend.services.local_store_service import (
    get_local_stores,
    create_local_store,
    add_local_store_product,
    get_local_products_for_master,
)

router = APIRouter(tags=["Local Stores"])


@router.get("/localstores")
def list_local_stores(search: Optional[str] = Query(None, description="Filter by location text")):
    # BUG FIX: was querying by 'city' which doesn't exist; now 'location'
    try:
        data = get_local_stores(search)
        return {"count": len(data), "stores": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/localstores", status_code=201)
def add_local_store(payload: LocalStoreIn):
    try:
        result = create_local_store(**payload.model_dump())
        return {"message": "Store created", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/localstoreproducts", status_code=201)
def add_local_store_product_route(payload: LocalStoreProductIn):
    try:
        result = add_local_store_product(**payload.model_dump())
        return {"message": "Local store product added", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/localstoreproducts/{master_product_id}")
def get_local_products_route(master_product_id: str):
    try:
        data = get_local_products_for_master(master_product_id)
        return {"master_product_id": master_product_id, "count": len(data), "local_listings": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
