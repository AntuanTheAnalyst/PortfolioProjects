import requests
import os
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")  # YOUR API KEY
account_sid = "YOUR_SID"
auth_token = os.environ.get("AUTH_TOKEN")  # YOUR TOKEN


weather_params = {
    "lat": 43.733994, # Sibenik, Croatia
    "lon": 15.895068,
    "appid": api_key,
    "cnt": 4
}
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()


will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data['weather'][0]['id']
    print(condition_code)
    if int(condition_code) < 700:
        will_rain = True


if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_='+14804280662',
        to='YOUR NUMBER'
    )

    # print(message.sid)
    print(message.status)
