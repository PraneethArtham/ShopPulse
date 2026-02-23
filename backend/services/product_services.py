import uuid
from dbase.supabase_client import supabase
from services.master_products import get_or_create_master_product


def insert_platform_product(
    product_name: str,
    price: float,
    platform_name: str,
    seller_id=None,
    rating=None,
    product_url=None,
    image_url=None,
    category="General"
):
    # auto‑map to master product
    master_product_id = get_or_create_master_product(
        product_name,
        category=category
    )

    data = {
        "platform_product_id": str(uuid.uuid4()),
        "master_product_id": master_product_id,
        "seller_id": seller_id,
        "platform_name": platform_name,
        "product_name": product_name,
        "price": price,
        "rating": rating,
        "product_url": product_url,
        "image_url": image_url
    }

    supabase.table("platform_products").insert(data).execute()

    return data

def delete_platform_product(platform_product_id: str):
    response = (
        supabase.table("platform_products")
        .delete()
        .eq("platform_product_id", platform_product_id)
        .execute()
    )
    return response


def get_platform_products():
    response = (
        supabase.table("platform_products")
        .select("*")
        .execute()
    )
    return response.data

def get_platform_products(product_name: str):
    response = (
        supabase.table("platform_products")
        .select("*")
        .ilike("product_name", f"%{product_name}%")
        .execute()
    )
    return response.data


def get_all_products():
    response = supabase.table("master_products").select("*").execute()
    return response.data

from dbase.supabase_client import supabase


def get_all_platform_products(
    platform: str = None,
    page: int = 1,
    limit: int = 10,
    sort: str = None
):
    query = supabase.table("platform_products").select("*")

    # 🔎 Filter by platform
    if platform:
        query = query.eq("platform_name", platform)

    # 🔢 Sorting
    if sort == "price_asc":
        query = query.order("price", desc=False)
    elif sort == "price_desc":
        query = query.order("price", desc=True)

    # 📄 Pagination
    start = (page - 1) * limit
    end = start + limit - 1
    query = query.range(start, end)

    response = query.execute()

    return response.data