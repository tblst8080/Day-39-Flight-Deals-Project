import requests
from flight_search import FlightSearch

class DataManager:
    def __init__(self, location_finder:FlightSearch):
        self.locator = location_finder
        self.endpoint = 'https://api.sheety.co/07ba30f9f4b8e27229537eb7b5dd282a/flightDeals/prices'
        self.token = "a189189e2812e"
        self.auth = {
            'Authorization': 'Bearer a189189e2812e'
        }

        # Updated JSON copy of Google Doc
        self.content = None

    def fill_iata(self):
        """Fill in """
        self.refresh()
        for item in self.content['prices']:

            # If row does not have iataCode:
            if item['iataCode'] == '':

                # Find the code based on city name
                city_code = self.locator.find_code(item['city'])

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
        return {row['iataCode']:row['lowestPrice'] for row in self.content['prices']}

    def update_price(self, catalog:dict):
        """Update Google Doc with the new lowest price. Takes FlightData catalog as input"""
        self.refresh()

        # Look through the rows:
        for destination in self.content['prices']:

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
        self.content = response.json()

    # TODO: New Function input subscriber info onto Google Doc
    # TODO: New function adds subscriber departure city to Google Doc, if not present

# TODO: 1) Add user departure city to the main list
# TODO: 2) search flights between all destinations in list
# TODO: 3) from the flights found, select ones with matching departure city to email to each user