from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, time
import pyautogui

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://elgoog.im/dinosaur-game/")

sleep(3)

game_area = driver.find_element(By.TAG_NAME, 'body')
game_area.send_keys(Keys.SPACE)

# Dino reference
dino_x = 69
dino_y = 746

# Detection point in front of dino, you can adjust depending on your screen size!
check_x = dino_x + 340

last_jump_time = 0
jump_cooldown = 0.12

while True:
    screenshot = pyautogui.screenshot()

    # Obstacle detection
    ground_pixels = [
        screenshot.getpixel((check_x, dino_y)),
        screenshot.getpixel((check_x + 10, dino_y)),
        screenshot.getpixel((check_x + 20, dino_y)),
    ]

    # Bird detection
    bird_pixels = [
        screenshot.getpixel((check_x, dino_y - 60)),
        screenshot.getpixel((check_x + 10, dino_y - 60)),
        screenshot.getpixel((check_x + 20, dino_y - 60)),
    ]

    current_time = time()

    # Bird: jump
    if any(p[0] < 200 for p in bird_pixels):
        if current_time - last_jump_time > jump_cooldown:
            game_area.send_keys(Keys.SPACE)
            last_jump_time = current_time

    # Cactus: jump
    elif any(p[0] < 200 for p in ground_pixels):
        if current_time - last_jump_time > jump_cooldown:
            game_area.send_keys(Keys.SPACE)
            last_jump_time = current_time