import requests
from datetime import datetime
import time
import smtplib

MY_EMAIL = "YOUR_EMAIL"
MY_PASSWORD = "YOUR_PASSWORD"

MY_LAT = 41.008240
MY_LONG = 28.978359


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])

    # Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT +5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    print(data)
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split("T")[1].split(":")[0])

    print(sunrise)
    print(sunset)

    time_now = datetime.now().hour

    if time_now >= sunset and time_now <= sunrise:
        return True # It's dark


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:Look Up!\n\nThe ISS is above you in the sky."
            )


