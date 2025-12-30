# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Search for Flights ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights)

    if not cheapest_flight or not cheapest_flight.price or cheapest_flight.price == "N/A":
        print(f"No valid flight data for {destination['city']}. Skipping.")
        continue

    print(f"{destination['city']}: £{cheapest_flight.price}")

    if float(cheapest_flight.price) < float(destination["lowestPrice"]):
        notification_manager.send_message(
            cheapest_flight.price,
            cheapest_flight.origin_airport,
            cheapest_flight.destination_airport,
            cheapest_flight.out_date,
            cheapest_flight.return_date
        )

    time.sleep(2)
