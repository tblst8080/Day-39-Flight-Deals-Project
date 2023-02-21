from flight_search import FlightSearch
import datetime as dt
from dateutil import tz

def convert_time(fUTC):
    """Convert UTC formatted time to datetime object"""
    fUTC = fUTC.replace("T", " " ).replace(".000Z", "")
    date_time = dt.datetime.strptime(f"{fUTC}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.gettz('UTC'))
    return date_time

class FlightData:
    """This class searches for cheap flights and stores them as dictionaries nested in a list"""

    def __init__(self, searcher:FlightSearch):
        self.flight_seeker = searcher

        # Catalog all the flights found
        self.my_flights = []   # TODO: New structure: [{email:, flights:[]}

    def search_flight(self, destinations:dict):
        """Search 6-month flights for each destination. Updates Google sheet with the lowest prices"""

        # TODO: search flights among all destinations:
        # Find flights below lowest price threshold for each destination
        for iataCode, lowestPrice in destinations.items():
            # Look for flights for each destination
            flights_found = self.flight_seeker.lookup_flights(destination=iataCode, lowest_price=lowestPrice)

            # Generate new dictionary item for each flight
            for flight in flights_found:

                # Pull out relevant information
                flight_info = {
                    't_iata': flight['cityCodeTo'],
                    'f_city': flight['cityFrom'],
                    'f_airport': flight['flyFrom'],
                    't_city': flight['cityTo'],
                    't_airport': flight['flyTo'],
                    'price': flight['price'],
                    'departure':convert_time(fUTC=flight['utc_departure']),  # Departure time in datetime
                    'return':convert_time(fUTC=flight['utc_arrival'])+dt.timedelta(days=flight['nightsInDest']),  # Return time in datetime
                    'link':flight['deep_link'],
                }

                # Add flight to list
                self.my_flights.append(flight_info)



