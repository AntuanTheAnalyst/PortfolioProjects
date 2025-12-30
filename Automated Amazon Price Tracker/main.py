import requests
from bs4 import BeautifulSoup
import smtplib
import os
import html
from email.message import EmailMessage

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

URL = ("https://www.amazon.com/Instant-Pot-Multi-Use-Pressure-Cooker/dp/B08WCLJ7JG/ref=sr_1_5?crid=3IOULF41JX90H&dib"
       "=eyJ2IjoiMSJ9.we9CUOoTRVFJeSc3LwbdF1z9cAQPsClFFm8Xii1yn1TBzg-J83tNfrYOmJMdsz7iKMYZgJn4x334WgpGUC8fApSim"
       "-cM3OlDm6IvnyMDdEmO85AAo7O_rElkXq9274Qx8FOWTbjSBkq5w7EDqtaNeWi4Gtp_"
       "S2rt128ZKrH60oUcXKXkL4aEIQkNKolDkVuRIZ5RRbNs_"
       "GNOLQYtiOjxW-5XfYEkPdR9ATQood3s8Xc.WrPexs5VKv1y6MXHCrfkngyuHkMEm2STATfXzFoTagI&dib_tag=se&keywords"
       "=Instant%2BPot%2BDuo%2BPlus%2B3%2BQuart&qid=1747641000&sprefix="
       "instant%2Bpot%2Bduo%2Bplus%2B3%2Bquart%2Caps%2C176&sr=8-5&th=1")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
response = requests.get(URL, headers=headers)
# print("Status Code:", response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

# Saving the HTML to see the webpage that we are getting:
# with open("amazon_page.html", "w", encoding="utf-8") as f:
#     f.write(soup.prettify())

# PRICE-OF-PRODUCT
price_tag = soup.find(name="span", class_="a-offscreen").getText()
price = float(price_tag.split("$")[1])

# TITLE-OF-PRODUCT
title_tag = soup.find_all(name="span", class_="a-size-base")[1]
title = html.unescape(title_tag.get_text(strip=True))

print(f"Title: {title}\nPrice: {price}")

# ====================== Send an Email ===========================

if price < 150:
    msg = EmailMessage()
    msg["Subject"] = "Amazon Price Alert!"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL
    msg.set_content(f"{title} is now ${price}\n{URL}")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.send_message(msg)
