import requests
from datetime import datetime
import os

GENDER = "female"
WEIGHT_KG = 60
HEIGHT_CM = 160
AGE = 25

today = datetime.now()
CURRENT_DATE = today.strftime("%d/%m/%Y")
CURRENT_TIME = today.strftime("%H:%M:%S")

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
exercise_endpoint = os.environ.get("EXERCISE_ENDPOINT")
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")

exercise_text = input("Enter your workout. Examples:\n-ran 3 miles\n-30 min weight lifting\n-30 min yoga\nYour data: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

exercise_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=exercise_params, headers=headers)
response.raise_for_status()
result = response.json()

input = "Ran 5K and cycled for 20 minutes"

for exercise in result['exercises']:
    exercise_name = exercise['name']
    duration_min = exercise['duration_min']
    calories = exercise['nf_calories']    

    sheet_inputs = {
        "sheet1": {
            "date": CURRENT_DATE,
            "time": CURRENT_TIME,
            "exercise": exercise_name,
            "duration": duration_min,
            "calories": calories,
        }
    }

    
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=(USER_NAME, PASSWORD))
    sheet_response.raise_for_status()

    print(sheet_response.text)

