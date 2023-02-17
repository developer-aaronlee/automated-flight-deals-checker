import requests
from flight_data import FlightData
from pprint import pprint

tequila_url = "https://tequila-api.kiwi.com/"
tequila_api_key = "3qSbW1TbCciqb7cOcM6bqxEhw1O3vKM3"

tequila_header = {
    "apikey": tequila_api_key,
    "Content-Type": "application/json"
}


class FlightSearch:

    def get_destination_code(self, city_name):
        location_params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=f"{tequila_url}locations/query", params=location_params, headers=tequila_header)
        response.raise_for_status()
        data = response.json()
        code = data["locations"][0]["code"]
        return code

    def check_flight(self, code, from_time, to_time):
        search_params = {
            "fly_from": "IAD",
            "fly_to": code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "USD",
            "max_stopovers": 0,
            "limit": 1
        }
        response = requests.get(url=f"{tequila_url}v2/search", params=search_params, headers=tequila_header)

        try:
            data = response.json()["data"][0]
            print(f"{data['route'][0]['cityTo']}: ${data['price']}")
        except IndexError:
            # print(f"No flights found for {code}")
            search_params["max_stopovers"] = 2
            response = requests.get(url=f"{tequila_url}v2/search", params=search_params, headers=tequila_header)
            data = response.json()["data"][0]
            print(f"{data['route'][1]['cityTo']}: ${data['price']}")
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                via_city=data["route"][0]["cityTo"],
                via_airport=data["route"][0]["flyTo"],
                stop_overs=1
            )

            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data



