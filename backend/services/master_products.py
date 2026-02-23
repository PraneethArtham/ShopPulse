import uuid
from dbase.supabase_client import supabase


def extract_brand(product_name: str):
    # simple heuristic: first word as brand
    return product_name.split()[0]


def get_or_create_master_product(product_name: str, category="General"):
    result = (
        supabase.table("master_products")
        .select("*")
        .ilike("product_name", product_name)
        .execute()
    )

    if result.data:
        return result.data[0]["master_product_id"]

    brand = extract_brand(product_name)

    new_product = {
        "master_product_id": str(uuid.uuid4()),
        "product_name": product_name,
        "brand": brand,
        "category": category,
        "description": f"{product_name} product"
    }

    supabase.table("master_products").insert(new_product).execute()

    return new_product["master_product_id"]


def get_all_categories():
    response = supabase.table("master_products")\
        .select("category")\
        .execute()

    categories = list(
        set([item["category"] for item in response.data if item["category"]])
    )

    return categories


def get_products_by_category(category: str, page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit - 1

    response = supabase.table("master_products")\
        .select("*")\
        .eq("category", category)\
        .range(start, end)\
        .execute()

    return response.data


def search_products(query: str, page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit - 1

    response = supabase.table("master_products")\
        .select("*")\
        .ilike("product_name", f"%{query}%")\
        .range(start, end)\
        .execute()

    return response.data