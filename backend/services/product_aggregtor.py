from dbase.supabase_client import supabase
def get_product_full_details(master_product_id: str):

    # 1. Get master product
    product = supabase.table("master_products")\
        .select("*")\
        .eq("master_product_id", master_product_id)\
        .single()\
        .execute()

    # 2. Get platform listings
    platforms = supabase.table("platform_products")\
        .select("*")\
        .eq("master_product_id", master_product_id)\
        .execute()

    platform_data = []

    for item in platforms.data:

        # 3. Get seller info
        seller = supabase.table("sellers")\
            .select("*")\
            .eq("seller_id", item["seller_id"])\
            .single()\
            .execute()

        # 4. Get reviews
        reviews = supabase.table("reviews")\
            .select("*")\
            .eq("platform_product_id", item["platform_product_id"])\
            .execute()

        item["seller"] = seller.data
        item["reviews"] = reviews.data

        platform_data.append(item)

    # 5. Get local stores
    local_products = supabase.table("local_store_products")\
        .select("*")\
        .eq("master_product_id", master_product_id)\
        .execute()

    local_data = []

    for item in local_products.data:
        store = supabase.table("local_stores")\
            .select("*")\
            .eq("store_id", item["store_id"])\
            .single()\
            .execute()

        item["store"] = store.data
        local_data.append(item)

    return {
        "product": product.data,
        "platform_listings": platform_data,
        "local_store_listings": local_data
    }