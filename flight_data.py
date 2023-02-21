class FlightData:
    """This class searches for cheap flights and stores them as dictionaries nested in a list"""

    def __init__(self, flight_info:dict):
        self.cityFrom = flight_info['cityFrom']
        self.iataFrom = flight_info['iataFrom']
        self.airportFrom = flight_info['airportFrom']

        self.stopover = flight_info['stopover']
        self.via_city = flight_info['via_city']

        self.cityTo = flight_info['cityTo']
        self.iataTo = flight_info['iataTo']
        self.airportTo = flight_info['airportTo']


        self.departure_flight = flight_info['departure']
        self.return_flight = flight_info['return']

        self.price = flight_info['price']
        self.link = flight_info['link']


