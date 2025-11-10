from selenium import webdriver
from twitter_bot import InternetSpeedTwitterBot

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# Initialising the Object
bot = InternetSpeedTwitterBot(driver)

bot.get_internet_speed()
bot.tweet_at_provider()
