#This file will need to use the Destination,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from sheetyAPI import Destination, Subscriber
from flight_matrix import PriceMatrix
from flight_data import FlightData
from sms_smtp import NotificationManager
from tequilaAPI import FlightSearch
import datetime as dt
from dateutil import tz


def convert_time(fUTC):
    """Convert UTC formatted time to datetime object"""
    fUTC = fUTC.replace("T", " " ).replace(".000Z", "")
    date_time = dt.datetime.strptime(f"{fUTC}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.gettz('UTC'))
    return date_time


def search_flight(routes: list, output:dict, discreet=False):
    """Search 6-month flights for each destination. Updates Google sheet with the lowest prices"""

    # TODO: search flights among all destinations:
    # Search flights for each route
    for route in routes:

        # Iterate search with 0 or 1 stopovers
        for stopover_num in range(0, 3):
            if not discreet:
                print(f"Looking for flights from {route['origin']} to {route['destination']} with {stopover_num} stopovers...")

            flights_found = my_flight_finder.lookup_flights(origin=route['origin'], destination=route['destination'],
                                                              lowest_price=route['price'], stopovers=stopover_num)
            # If flights are found:
            if len(flights_found) > 0:
                key = (route['origin'], route['destination'])
                # Add entry in catalog
                output[key] = []

                # Add flight info to the catalog
                for flight in flights_found:
                    if stopover_num > 0:
                        transit = [stops['cityFrom'] for stops in flight['route'][1:-1]]
                        transit = ', '.join(transit)
                    else:
                        transit = " "

                    # Pull out relevant information
                    flight_info = {
                        'iataTo': flight['cityCodeTo'],
                        'iataFrom': flight['cityCodeFrom'],
                        'cityFrom': flight['cityFrom'],
                        'airportFrom': flight['flyFrom'],
                        'stopover': stopover_num,
                        'via_city': transit,
                        'cityTo': flight['cityTo'],
                        'airportTo': flight['flyTo'],
                        'price': flight['price'],
                        'departure': convert_time(fUTC=flight['utc_departure']),  # Departure time in datetime
                        'return': convert_time(fUTC=flight['utc_arrival']) + dt.timedelta(days=flight['nightsInDest']),
                        # Return time in datetime
                        'link': flight['deep_link'],
                    }

                    # Add flight to list
                    output[key].append(FlightData(flight_info=flight_info))

                # Stop searching flights for the route
                break

def refine_price():
    print('Refining prices..')
    search_flight(routes=route_matrix.routes, output=all_flights, discreet=True)
    route_matrix.update_prices(catalog=all_flights, discreet=True)


# Setting up objects
my_flight_finder = FlightSearch()
my_notifier = NotificationManager()
subscribers = Subscriber()
destinations = Destination()


# Fill IATA information for new cities in sheet
print('Filling IATA codes...')
destinations.fill_iata(location_finder=my_flight_finder)
subscribers.fill_iata(location_finder=my_flight_finder)


# Update all the routes to search for
print("Updating routes...")
route_matrix = PriceMatrix(dest_obj=destinations, sub_obj=subscribers)
route_matrix.fill_matrix()
route_matrix.generate_routes()

# Generate container object for flight information
all_flights = {}

# refine_price()

# Search for available flights
print('Searching for flights...')
search_flight(routes=route_matrix.routes, output=all_flights)

# Update lowest price on google doc
print('Updating prices...')
route_matrix.update_prices(catalog=all_flights)

# Send notification via email
print('Sending results...')
my_notifier.send_email(catalog=all_flights, subscription_list=subscribers.content)



