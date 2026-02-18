from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Shop Pulse API running"}


@app.get("/products")
def get_products():
    response = supabase.table("platform_products").select("*").execute()
    return response.data
