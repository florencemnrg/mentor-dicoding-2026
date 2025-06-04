import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"
}

def extract_product_data(prod_div):
    product_name_tag = prod_div.find("h3", class_="product-title")
    product_name = product_name_tag.text.strip() if product_name_tag else ""

    price_span = prod_div.select_one("div.price-container > span.price")
    price_p = prod_div.find("p", class_="price")
    if price_span:
        price = price_span.text.strip()
    elif price_p:
        price = price_p.text.strip()
    else:
        price = "Price Unavailable"

    data = {
        "Product Name": product_name,
        "Price": price
    }

    p_tags = prod_div.find_all("p")
    for p in p_tags:
        if p.get("class") == ["price"]:
            continue
        text = p.text.strip()
        if ":" in text:
            key, val = text.split(":", 1)
            data[key.strip()] = val.strip()
        else:
            match = re.search(r'(\d+)', text)
            if match:
                data['Color'] = int(match.group(1))
            else:
                data['Color'] = None

    return data

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_products_from_page(url):
    content = fetch_page_content(url)
    if not content:
        return []

    soup = BeautifulSoup(content, "html.parser")
    products = []
    for prod_div in soup.find_all("div", class_="product-details"):
        product_data = extract_product_data(prod_div)
        products.append(product_data)

    return products

def extract_all_pages(base_url, pages=50):
    all_products = []
    for page_num in range(1, pages + 1):
        url = base_url if page_num == 1 else f"{base_url}page{page_num}"
        print(f"Scraping page {page_num} from {url}...")
        products = scrape_products_from_page(url)
        all_products.extend(products)
        time.sleep(1)
    return pd.DataFrame(all_products)
