import requests

sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ai9f034mfpslmf3f09j302"
}

sheety_prices_url = "https://api.sheety.co/5081303fda5ac7c15023a7f07cf98314/flightDeals/prices"
sheety_users_url = "https://api.sheety.co/5081303fda5ac7c15023a7f07cf98314/flightDeals/users"

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.user_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_prices_url, headers=sheety_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for x in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": x["iataCode"]
                }
            }
            response = requests.put(url=f"{sheety_prices_url}/{x['id']}", json=new_data, headers=sheety_headers)
            # print(response.text)

    def get_user_data(self):
        response = requests.get(url=sheety_users_url, headers=sheety_headers)
        response.raise_for_status()
        data = response.json()
        self.user_data = data["users"]
        return self.user_data

