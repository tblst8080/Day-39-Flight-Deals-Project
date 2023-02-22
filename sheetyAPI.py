import requests
from tequilaAPI import FlightSearch
from APIs import sheety_endpoint, sheety_token

class Destination:
    def __init__(self):
        self.endpoint = f'{sheety_endpoint}/flightDeals/prices'
        self.token = sheety_token # "a189189e2812e"
        self.auth = {
            'Authorization': f'Bearer {self.token}'
        }

        # Updated JSON copy of Google Doc
        self.content = None
        self.refresh()

    def fill_iata(self, location_finder:FlightSearch):
        """Fill in """
        for item in self.content:

            # If row does not have iataCode:
            try:
                item['iataCode']

            except:

                # Find the code based on city name
                city_code = location_finder.find_code(item['city'])

                # Package the code found
                payload = {
                    'price':{
                        'iataCode': city_code
                    }
                }

                # Update row with IATA info
                put_endpoint = f"{self.endpoint}/{item['id']}"
                requests.put(url=put_endpoint, json=payload, headers=self.auth)
        self.refresh()

    def refresh(self):
        """Update JSON copy of Google Doc sheet"""
        response = requests.get(url=self.endpoint, headers=self.auth)
        self.content = response.json()['prices']


class Subscriber:
    def __init__(self):
        self.endpoint = f'{sheety_endpoint}/flightDeals/subscribers'
        self.token = sheety_token
        self.auth = {
            'Authorization': f'Bearer {self.token}'
        }

        # Updated JSON copy of Google Doc
        self.content = None
        self.refresh()

    def add_user(self, first_name, last_name, email, origin, iata):
        # Package the code found
        if email not in [row['email'] for row in self.content]:
            payload = {
                'subscriber':{
                    'firstName':first_name,
                    'lastName':last_name,
                    'email':email,
                    'origin':origin,
                    'iataCode': iata
                }
            }

            # Update row with IATA info
            response = requests.post(url=self.endpoint, json=payload, headers=self.auth)
            return True
        else:
            return False

    def fill_iata(self, location_finder:FlightSearch):
        """Fill in """
        for item in self.content:

            # If row does not have iataCode:
            try:
                item['iataCode']

            except:
                # Find the code based on city name
                city_code = location_finder.find_code(item['origin'])

                # Package the code found
                payload = {
                    'subscriber':{
                        'iataCode': city_code
                    }
                }

                # Update row with IATA info
                put_endpoint = f"{self.endpoint}/{item['id']}"
                requests.put(url=put_endpoint, json=payload, headers=self.auth)
        self.refresh()

    def refresh(self):
        """Update JSON copy of Google Doc sheet"""
        response = requests.get(url=self.endpoint, headers=self.auth)
        self.content = response.json()['subscribers']
