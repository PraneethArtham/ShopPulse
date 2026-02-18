import uuid
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# USER INPUT
# -----------------------------
search_query = input("Enter product to search: ").strip()

# -----------------------------
# SELENIUM SETUP
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(f"https://www.flipkart.com/search?q={search_query}")
time.sleep(4)

# Close login popup if it appears
try:
    close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
    close_btn.click()
    print("Popup closed")
except:
    pass

time.sleep(2)

items = driver.find_elements(By.CLASS_NAME, "_1AtVbE")
print("Items found:", len(items))

count = 0

for item in items:
    try:
        # Layout 1 (electronics/products)
        try:
            name = item.find_element(By.CLASS_NAME, "s1Q9rs").text
        except:
            # Layout 2 (general products like groceries)
            name = item.find_element(By.CLASS_NAME, "IRpwTa").text

        price = item.find_element(By.CLASS_NAME, "_30jeq3").text

        product_data = {
            "platform_product_id": str(uuid.uuid4()),
            "master_product_id": None,
            "seller_id": None,
            "platform_name": "Flipkart",
            "product_name": name,
            "price": float(price.replace("₹", "").replace(",", "")),
            "rating": None,
            "product_url": None,
            "image_url": None,
            "created_at": datetime.now().isoformat()
        }

        supabase.table("platform_products").insert(product_data).execute()
        print("Inserted:", name)

        count += 1
        if count == 10:
            break

    except:
        pass


driver.quit()

print("Done inserting products into Supabase.")
