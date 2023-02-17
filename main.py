from datetime import datetime, timedelta
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager


def date_calculator(date, delta):
    new_date_obj = date + timedelta(delta)
    new_date = new_date_obj.strftime("%d/%m/%Y")
    return new_date


data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()
# print(sheet_data)

for x in sheet_data:
    x["iataCode"] = flight_search.get_destination_code(x["city"])
# print(sheet_data)

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

destinations = {x["iataCode"]: {"id": x["id"], "city": x["city"], "price": x["lowestPrice"]} for x in sheet_data}
pprint(destinations)

today = datetime.now()
date_from = date_calculator(today, 1)
date_to = date_calculator(today, 180)

for x in destinations:
    flight = flight_search.check_flight(code=x, from_time=date_from, to_time=date_to)
    if flight.price < destinations[x]["price"]:

        user_data = data_manager.get_user_data()
        user_emails = [x["email"] for x in user_data]

        message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to " \
                f"{flight.destination_city}-{flight.destination_airport} from {flight.out_date} to {flight.return_date}"

        if flight.stop_overs == 1:
            message += f"\nFlight has 1 stopover, via {flight.via_city}-{flight.via_airport}"

        notification_manager.send_message(message)

        link = f"\nhttps://www.google.com/travel/flights?q=Flights%20to%20{flight.destination_airport}%20from%20" \
               f"{flight.origin_airport}%20on%20{flight.out_date}%20through%20{flight.return_date}"

        notification_manager.send_email(user_emails, message, link)

