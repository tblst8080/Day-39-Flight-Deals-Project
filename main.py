#This file will need to use the Destination,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from sheetyAPI import Destination
from flight_data import FlightData
from tequilaAPI import FlightSearch
from sms_smtp import NotificationManager

# Setting up objects
my_flight_finder = FlightSearch()
my_google_doc = Destination(location_finder=my_flight_finder)
my_notifier = NotificationManager()


# TODO: Fill IATA information on user page first and add it to the search sheet
# Fill IATA information for new cities in sheet
print('Filling IATA codes...')
my_google_doc.fill_iata()

# Search for flights for all cities
my_destinations = my_google_doc.update_destinations()  # Generate a dictionary containing all destinations {iataCode;lowestPrice}

# Generate container object for flight information
my_flight_data = FlightData(searcher=my_flight_finder)

# Search for available flights
print('Searching for flights...')
my_flight_data.search_flight(destinations=my_destinations)

# Update lowest price on google doc
print('Updating prices...')
my_google_doc.update_price(catalog=my_flight_data.my_flights)

# Send notification via email
print('Sending results...')
my_notifier.send_email(catalog=my_flight_data.my_flights)



