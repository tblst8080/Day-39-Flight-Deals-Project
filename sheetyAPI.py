import requests
from tequilaAPI import FlightSearch

class Destination:
    def __init__(self):
        self.endpoint = 'https://api.sheety.co/07ba30f9f4b8e27229537eb7b5dd282a/flightDeals/prices'
        self.token = "a189189e2812e"
        self.auth = {
            'Authorization': 'Bearer a189189e2812e'
        }

        # Updated JSON copy of Google Doc
        self.content = None
        self.refresh()

    def fill_iata(self, location_finder:FlightSearch):
        """Fill in """
        self.refresh()
        for item in self.content:

            # If row does not have iataCode:
            if item['iataCode'] == '':

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

    def update_destinations(self) -> dict:
        """Retrieve destination (IATA Code) and lowest price (USD) data from Google Doc"""
        self.refresh()
        return {row['iataCode']:row['lowestPrice'] for row in self.content}

    def update_price(self, catalog:dict):
        """Update Google Doc with the new lowest price. Takes FlightData catalog as input"""
        self.refresh()

        # Look through the rows:
        for destination in self.content:

            # Generate prices corresponding to IATA
            prices = [flight['price'] for flight in catalog if flight['t_iata'] == destination['iataCode']]

            # If lower price is found:
            if len(prices)>0:

                new_low = min(prices)

                # Create payload
                payload = {
                    'price':{
                        'lowestPrice': new_low
                    }
                }

            else:
                old_price = destination['lowestPrice']
                payload = {
                    'price':{
                        'lowestPrice': old_price * 1.1
                    }
                }
            # Update endpoint with cell number
            put_endpoint = f"{self.endpoint}/{destination['id']}"

            # Edit value in cell
            requests.put(url=put_endpoint, json=payload, headers=self.auth)

    def refresh(self):
        """Update JSON copy of Google Doc sheet"""
        response = requests.get(url=self.endpoint, headers=self.auth)
        self.content = response.json()['prices']

    # TODO: New Function input subscriber info onto Google Doc
    # TODO: New function adds subscriber departure city to Google Doc, if not present

class Subscriber:
    def __init__(self):
        self.endpoint = 'https://api.sheety.co/07ba30f9f4b8e27229537eb7b5dd282a/flightDeals/subscribers'
        self.token = "a189189e2812e"
        self.auth = {
            'Authorization': 'Bearer a189189e2812e'
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
            requests.post(url=self.endpoint, json=payload, headers=self.auth)
        else:
            print("Email is already in the system. Please enter another one.")

    def refresh(self):
        """Update JSON copy of Google Doc sheet"""
        response = requests.get(url=self.endpoint, headers=self.auth)
        self.content = response.json()['subscribers']



# TODO: 1) Add user departure city to the main list
# TODO: 2) search flights between all destinations in list
# TODO: 3) from the flights found, select ones with matching departure city to email to each user