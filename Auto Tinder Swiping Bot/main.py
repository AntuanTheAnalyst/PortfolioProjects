from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import time

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

URL = "https://tinder.com/"

load_dotenv()

phone_number = os.getenv("PHONE_NUMBER")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
time.sleep(3)

# Declining cookies
decline_button = driver.find_element(By.XPATH, "//button[.//div[text()='I decline']]")
decline_button.click()

# Log in
login_link = driver.find_element(By.XPATH, "//a[.//div[text()='Log in']]")
login_link.click()
time.sleep(5)

phone_number_field = driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) button div div div div div")
phone_number_field.click()
time.sleep(5)

country_code_menu = driver.find_element(By.XPATH, "//div[@aria-label='Select your phone country code']")
country_code_menu.click()
time.sleep(5)

georgia_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Georgia') or contains(text(), '+995')]")
georgia_option.click()
time.sleep(5)

phone_number_input = driver.find_element(By.ID, "phone_number")
phone_number_input.send_keys(phone_number)
time.sleep(5)

next_button = driver.find_element(By.XPATH, "//div[text()='Next']/ancestor::button")
next_button.click()
# Pause to allow manual CAPTCHA completion
input("Please complete the CAPTCHA manually and press Enter to continue...")

# Allowing location services
time.sleep(5)
loc_services = driver.find_element(By.CSS_SELECTOR, "button:nth-child(1) div div div")
loc_services.click()
time.sleep(5)

# Clicking not interested in notifications
notif_off = driver.find_element(By.XPATH, '//*[@id="o-853424009"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]/div')
notif_off.click()
time.sleep(5)

for _ in range(10):
    try:
        swipe_left = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(2) button span span.gamepad-icon-wrapper')
        try:
            swipe_left.click()
            time.sleep(7)
        except ElementClickInterceptedException:
            print("Match pop-up detected. Trying to close it...")
            try:
                back_to_tinder = driver.find_element(By.XPATH, "//button[contains(., 'Back to Tinder')]")
                back_to_tinder.click()
                print("Closed the match popup.")
                time.sleep(3)
            except NoSuchElementException:
                print("Back to Tinder button not found.")
    except NoSuchElementException:
        print("Swipe button not found.")
        time.sleep(7)



# Changing window
# base_window = driver.window_handles[0]
# fb_login_window = driver.window_handles[1]
# driver.switch_to.window(fb_login_window)
# print(driver.title)
