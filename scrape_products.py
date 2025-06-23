from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3
import time
import os

# --- Setup database ---
conn = sqlite3.connect("products.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    sku TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    url TEXT,
    location TEXT
)
""")

# --- Selenium setup ---
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Point to chromedriver.exe
service = Service(os.path.join(os.getcwd(), "chromedriver.exe"))
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Scrape individual product page ---
def scrape_product(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.select_one('span.base')
    description = soup.select_one('div.product.attribute.description')
    sku_el = soup.select_one('div.product.attribute.sku span')

    if title and sku_el:
        return {
            'title': title.text.strip(),
            'sku': sku_el.text.strip(),
            'description': description.text.strip() if description else '',
            'url': url
        }
    return None

# --- Scrape category with JS-rendered content ---
def scrape_category(base_url):
    page = 1
    while True:
        print(f"Scraping page {page} of: {base_url}")
        paged_url = f"{base_url}?p={page}"
        driver.get(paged_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-item-link"))
            )
        except:
            print("No more products or page didn't load properly.")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.select('a.product-item-link')
        if not links:
            break

        print(f"Found {len(links)} products on page {page}")

        for a in links:
            product_url = a['href'].split('?')[0]
            try:
                product = scrape_product(product_url)
                if product:
                    c.execute("""
                        INSERT OR REPLACE INTO products (sku, title, description, url, location)
                        VALUES (?, ?, ?, ?, COALESCE((SELECT location FROM products WHERE sku = ?), ''))
                    """, (product['sku'], product['title'], product['description'], product['url'], product['sku']))
                    conn.commit()
                    print(f"Added {product['sku']}: {product['title']}")
                time.sleep(1)
            except Exception as e:
                print(f"Error with {product_url}: {e}")

        page += 1

# --- Start scraping ---
scrape_category("https://www.harveynorman.com.au/vacuum-laundry-appliances/vacuum-cleaners/vacuum-cleaners")
scrape_category("https://www.harveynorman.com.au/kitchen-appliances")

# --- Clean up ---
driver.quit()
conn.close()
print("Done.")
