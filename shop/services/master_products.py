import uuid
from db.supabase_client import supabase


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
