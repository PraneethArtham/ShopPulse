from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import re
from backend.dbase import supabase_client

# ================= DRIVER =================
driver = webdriver.Chrome()

query = input("Enter product name: ")

# =========================================================
# ================= AMAZON SCRAPER ========================
# =========================================================

print("\n===== AMAZON SCRAPING =====")

amazon_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
driver.get(amazon_url)
time.sleep(random.randint(5, 8))

links = driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")
amazon_links = [link.get_attribute("href") for link in links[:5]]

for url in amazon_links:

    if not url or "sspa" in url or "sponsored" in url:
        continue

    print("\n[Amazon] Opening:", url)
    driver.get(url)
    time.sleep(random.randint(4, 7))

    # ---------- TITLE ----------
    try:
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        ).text
    except:
        title = "Not Found"

    # ---------- PRICE ----------
    clean_price = None
    price_text = ""

    try:
        price_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-offscreen"))
        )
        price_text = price_element.text
    except:
        pass

    if not price_text:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price_span = soup.find("span", class_="a-offscreen")
        if price_span:
            price_text = price_span.text

    if not price_text:
        match = re.search(r"₹\s?[\d,]+", driver.page_source)
        if match:
            price_text = match.group()

    if price_text:
        try:
            clean_price = float(price_text.replace("₹", "").replace(",", "").strip())
        except:
            clean_price = None

    # ---------- RATING ----------
    try:
        rating_text = driver.find_element(
            By.XPATH, "//span[@data-hook='rating-out-of-text']"
        ).text
        rating = float(rating_text.split()[0])
    except:
        rating = None

    # ---------- IMAGE ----------
    image_url = None
    try:
        image_element = driver.find_element(By.ID, "landingImage")
        image_url = image_element.get_attribute("src")
    except:
        pass

    print("[Amazon]", title, clean_price)

    try:
        supabase.table("platform_products").insert({
            "product_name": title,
            "platform_name": "Amazon",
            "price": clean_price,
            "rating": rating,
            "product_url": url,
            "image_url": image_url
        }).execute()
    except Exception as e:
        print("Amazon DB Insert Failed:", e)

    time.sleep(random.randint(3, 6))

# =========================================================
# ================= FLIPKART SCRAPER ======================
# =========================================================

print("\n===== FLIPKART SCRAPING =====")

flipkart_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
driver.get(flipkart_url)
time.sleep(random.randint(5, 8))

# close login popup
try:
    close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
    close_btn.click()
    time.sleep(2)
except:
    pass

links = driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")

flipkart_links = []
for l in links:
    href = l.get_attribute("href")
    if href and href not in flipkart_links:
        flipkart_links.append(href)

flipkart_links = flipkart_links[:5]

for url in flipkart_links:

    print("\n[Flipkart] Opening:", url)
    driver.get(url)
    time.sleep(random.randint(4, 7))

    # ---------- TITLE ----------
    try:
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.VU-ZEz"))
        ).text
    except:
        title = "Not Found"

    # ---------- PRICE ----------
    clean_price = None
    try:
        price_text = driver.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text
        clean_price = float(price_text.replace("₹", "").replace(",", ""))
    except:
        clean_price = None

    # ---------- RATING ----------
    try:
        rating_text = driver.find_element(By.CSS_SELECTOR, "div.XQDdHH").text
        rating = float(rating_text)
    except:
        rating = None

    # ---------- IMAGE ----------
    image_url = None
    try:
        image_element = driver.find_element(By.CSS_SELECTOR, "img._396cs4")
        image_url = image_element.get_attribute("src")
    except:
        pass

    print("[Flipkart]", title, clean_price)

    try:
        supabase.table("platform_products").insert({
            "product_name": title,
            "platform_name": "Flipkart",
            "price": clean_price,
            "rating": rating,
            "product_url": url,
            "image_url": image_url
        }).execute()
    except Exception as e:
        print("Flipkart DB Insert Failed:", e)

    time.sleep(random.randint(3, 6))

driver.quit()
print("\n✅ DONE — BOTH PLATFORMS SCRAPED")