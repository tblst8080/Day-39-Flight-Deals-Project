import requests
import datetime as dt

class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self):
        self.endpoint = 'https://api.tequila.kiwi.com/v2/search'
        self.location = 'https://api.tequila.kiwi.com/locations/query'
        self.key = 'U35JJmxfcZzQ6oO840BUTELOaos7cntn'
        self.id = 'germsandspicesflightsearch'

        self.header = {'apikey': self.key}

    def lookup_flights(self, origin:str, destination:str, lowest_price:str, stopovers:int = 0):
        """Look up flights in the next six months and returns list of available flights under lowest_price"""

        # Calculate period for search
        tomorrow = dt.datetime.now() + dt.timedelta(days=1)
        deadline = tomorrow + dt.timedelta(days=100)

        # Setting parameters for flight search
        parameters = {
            'fly_from': f'city:{origin}',
            'fly_to': f'city:{destination}',
            'date_from': tomorrow.strftime("%d/%m/%Y"),
            'date_to': deadline.strftime("%d/%m/%Y"),
            'locale': 'en',
            'curr': 'USD',
            'price_to': f'{int(lowest_price)}',
            'max_stopovers': stopovers,
            'flight_type': 'round',
            'nights_in_dst_from':7,
            'nights_in_dst_to':28
        }

        response = requests.get(url=self.endpoint, params=parameters, headers=self.header)
        print(response.json())
        return response.json()['data']

    def find_code(self, city):
        """Given a city, returns its IATA code."""
        parameters = {
            'term': city,
            'locale':'en-US',
            'location_types':'city'
        }

        response = requests.get(url=self.location, params=parameters, headers = self.header)
        return response.json()['locations'][0]['code']
