from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import os

# Chrome options (optional but good)
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

URL = "https://www.audible.com/search?keywords=book&node=18573211011"
driver.get(URL)

wait = WebDriverWait(driver, 10)

wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "productListItem"))
)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

books = soup.find_all("li", class_="productListItem")

books_data = []
for book in books:
    # Title
    title_tag = book.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else None
    print(title)

    # Author
    author_tag = book.find("li", class_="authorLabel")
    author = author_tag.get_text(strip=True).replace("By:", "").strip() if author_tag else None

    # Price
    price_tag = book.find("p", class_="buybox-regular-price")
    price = price_tag.get_text(strip=True) if price_tag else None

    # Rating
    rating_tag = book.find("li", class_="ratingsLabel")
    rating = rating_tag.get_text(strip=True) if rating_tag else None

    # Length
    length_tag = book.find("li", class_="runtimeLabel")
    length = length_tag.get_text(strip=True) if length_tag else None

    books_data.append({
        "title": title,
        "author": author,
        "price": price,
        "rating_raw": rating,
        "length_raw": length
    })

df = pd.DataFrame(books_data)

df.to_csv("audible_books.csv", index=False, encoding="utf-8")






