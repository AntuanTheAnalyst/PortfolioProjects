import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import time
import random

GOOGLE_FORM_URL = "https://forms.gle/VXzoKt3N9bMCw13B8"
ZILLOW_WEBSITE = "https://appbrewery.github.io/Zillow-Clone/"

# Scrape the links, addresses, and prices of the rental properties

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(ZILLOW_WEBSITE, headers=header)

zillow_webpage = response.text
soup = BeautifulSoup(zillow_webpage, "html.parser")

houses = soup.find_all(name="div", class_="StyledCard-c11n-8-84")

house_links = []
house_prices = []
house_addresses = []
for house in houses:
    links = house.find("a").get("href")
    house_links.append(links)
    prices = house.find("span").get_text()
    clean_prices = prices.strip("+ /mo 1bd")
    house_prices.append(clean_prices)

    addresses = house.find("address").get_text()
    clean_addresses = addresses.replace("\n", " ")
    clean_addresses = clean_addresses.replace(" |", ",")
    clean_addresses = clean_addresses.strip()
    clean_addresses = " ".join(clean_addresses.split())
    house_addresses.append(clean_addresses)


# Using Selenium and filling in the Google Form automatically
# Chrome Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM_URL)
time.sleep(3)

number = 0
for _ in range(len(house_prices)):
    questions = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    questions[0].send_keys(house_addresses[number])
    time.sleep(random.uniform(2, 5))
    questions[1].send_keys(house_prices[number])
    time.sleep(random.uniform(3, 6))
    questions[2].send_keys(house_links[number])
    time.sleep(random.uniform(2, 6))
    send_button = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][aria-label="Submit"]')
    send_button.click()
    time.sleep(random.uniform(2, 6))
    driver.find_element(By.LINK_TEXT, "Başka bir yanıt gönder").click()
    time.sleep(random.uniform(3, 8))
    number += 1

driver.quit()
