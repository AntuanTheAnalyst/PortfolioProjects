from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time
import random
from datetime import datetime
import smtplib

load_dotenv()

SIMILAR_ACCOUNT = "cristiano"
EMAIL = os.getenv("INSTAGRAM_EMAIL")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


class InstaFollower:
    def __init__(self):
        # Optional - Keep browser open (helps diagnose issues during a crash)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(5.3)

        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")

        username.send_keys(EMAIL)
        time.sleep(4.5)
        password.send_keys(PASSWORD)

        time.sleep(6.5)
        password.send_keys(Keys.ENTER)

        time.sleep(7.3)
        # Click "Not now" and ignore Save-login info prompt
        save_login_prompt = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()

        time.sleep(5.2)

    def find_followers(self):
        url = "https://www.instagram.com/chefsteps/"
        self.driver.get(url)
        time.sleep(5.4)

        self.driver.find_element(By.CSS_SELECTOR, "a[href='/chefsteps/followers/']").click()
        time.sleep(4.9)

        # Wait for the modal to open
        pop_up_window = self.driver.find_element(
            By.XPATH, '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
        time.sleep(4.7)

        while True:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                pop_up_window)
            time.sleep(random.uniform(1, 2))

    def follow(self):
        following_list = self.driver.find_elements(By.XPATH, "//button[.//div[text()='Follow']]")

        for person in following_list:
            try:
                person.click()
                time.sleep(random.uniform(2, 3))
            except ElementClickInterceptedException:
                try:
                    cancel_button = self.driver.find_element(By.XPATH, "//button[text()='Cancel']")
                    cancel_button.click()
                    time.sleep(3)
                except NoSuchElementException:
                    print("Cancel button not found. Skipping...")
                    continue





# Initialising the Object
bot = InstaFollower()
# Methods
bot.login()
bot.find_followers()
bot.follow()
