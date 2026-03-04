"""
backend/services/review_service.py

Actual DB columns:
  review_id, platform_product_id, review_text, review_rating,
  sentiment_score, is_fake, created_at
"""

import uuid
from typing import Optional
from backend.dbase.supabase_client import supabase


def add_review(
    platform_product_id: str,
    review_rating: float,
    review_text: Optional[str] = None,
    sentiment_score: Optional[float] = None,
    is_fake: bool = False,
) -> dict:
    # BUG FIX: use real column names (review_text/review_rating, not comment/rating)
    data = {
        "review_id": str(uuid.uuid4()),
        "platform_product_id": platform_product_id,
        "review_text": review_text,
        "review_rating": review_rating,
        "sentiment_score": sentiment_score,
        "is_fake": is_fake,
    }
    supabase.table("reviews").insert(data).execute()
    return data


def get_reviews_for_platform_product(platform_product_id: str) -> list:
    # BUG FIX: order by created_at not "date"
    return (
        supabase.table("reviews")
        .select("*")
        .eq("platform_product_id", platform_product_id)
        .order("created_at", desc=True)
        .execute()
        .data or []
    )


def get_all_reviews_for_master(master_product_id: str) -> list:
    platform_products = (
        supabase.table("platform_products")
        .select("platform_product_id, platform_name")
        .eq("master_product_id", master_product_id)
        .execute()
        .data or []
    )
    all_reviews = []
    for pp in platform_products:
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("platform_product_id", pp["platform_product_id"])
            .execute()
            .data or []
        )
        for r in reviews:
            r["platform_name"] = pp["platform_name"]
        all_reviews.extend(reviews)
    # BUG FIX: sort by created_at not "date"
    return sorted(all_reviews, key=lambda x: x.get("created_at", ""), reverse=True)
