from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

INT_SPEED_URL = "https://www.speedtest.net/"
TWITTER_URL = "https://x.com/"

PROMISED_DOWN = 150
PROMISED_UP = 10


class InternetSpeedTwitterBot:
    def __init__(self, driver):
        self.driver = driver
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get(INT_SPEED_URL)
        time.sleep(5)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(3)
        start_test = self.driver.find_element(By.CLASS_NAME, "js-start-test")
        start_test.click()
        time.sleep(50)

        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
        print(f"Download speed: {self.down} Mbps\nUpload speed: {self.up} Mbps")

    def tweet_at_provider(self):
        self.driver.get(TWITTER_URL)
        time.sleep(5)

        login = self.driver.find_element(By.LINK_TEXT, "Sign in")
        login.click()
        time.sleep(5)

        email_box = self.driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
        time.sleep(1)
        email_box.send_keys(email, Keys.ENTER)
        time.sleep(4)
        password_box = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_box.send_keys(password, Keys.ENTER)
        time.sleep(4)

        tweet_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"][contenteditable="true"]')
        tweet_box.click()
        message = (f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for "
                   f"{PROMISED_DOWN}down/{PROMISED_UP}up?")
        tweet_box.send_keys(message)

        time.sleep(2)
        self.driver.quit()

        print(f"\n✅ Tweet #1 ready:\n{message}")