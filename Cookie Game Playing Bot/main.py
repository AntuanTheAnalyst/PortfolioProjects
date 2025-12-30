from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import time

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
URL = "https://orteil.dashnet.org/experiments/cookie/"
driver.get(URL)

store_prices = driver.find_element(By.ID, value="store")
text = store_prices.text

five_sec_check = time() + 5
timeout = time() + 60  # 1 minute
while True:
    cookie = driver.find_element(By.ID, value="cookie")
    cookie.click()

    cookie_tag = driver.find_element(By.ID, value="money")
    cookies = float(cookie_tag.text.replace(",", ""))

    if time() > five_sec_check:
        upgrades = {
            "buyCursor": int(driver.find_element(By.ID, "buyCursor").text.split("-")[1].strip().split()[0]),
            "buyGrandma": int(driver.find_element(By.ID, "buyGrandma").text.split("-")[1].strip().split()[0]),
            "buyFactory": int(driver.find_element(By.ID, "buyFactory").text.split("-")[1].strip().split()[0]),
            "buyMine": int(
                driver.find_element(By.ID, "buyMine").text.split("-")[1].strip().split()[0].replace(",", "")),
            "buyShipment": int(
                driver.find_element(By.ID, "buyShipment").text.split("-")[1].strip().split()[0].replace(",", "")),
            "buyAlchemy lab": int(
                driver.find_element(By.ID, "buyAlchemy lab").text.split("-")[1].strip().split()[0].replace(",", "")),
            "buyPortal": int(
                driver.find_element(By.ID, "buyPortal").text.split("-")[1].strip().split()[0].replace(",", "")),
            "buyTime machine": int(
                driver.find_element(By.ID, "buyTime machine").text.split("-")[1].strip().split()[0].replace(",", ""))
        }

        affordable = {id: price for id, price in upgrades.items() if cookies >= price}

        if affordable:
            best_upgrade_id = max(affordable, key=affordable.get)
            driver.find_element(By.ID, best_upgrade_id).click()

        five_sec_check = time() + 5 # Reset the timeout

    if time() > timeout:
        break

cookies_per_sec = cookies / 60
print(f"Final Cookies: {cookies}")
print(f"Cookies/second: {cookies_per_sec:.2f}")

