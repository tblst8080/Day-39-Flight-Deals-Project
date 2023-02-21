import requests
from tequilaAPI import FlightSearch
from sheetyAPI import Subscriber

def check_origin(message):
    origin = input(message).title()
    code = my_searcher.find_code(origin)
    if not code:
        print()
        return check_origin("Invalid city name. Please enter another one: \n")
    else:
        return code, origin

print("Welcome to the Flight Club")

print('We find the best flight deals and email you.')

first_name = input("Please enter your first name: \n").title()

last_name = input("Please enter your last name: \n").title()

email = input("Please enter your email: \n")


my_searcher = FlightSearch()

iata, origin = check_origin("What city do you wish to depart from? \n")


my_uploader = Subscriber()
my_uploader.add_user(first_name = first_name, last_name=last_name, email=email, origin=origin, iata=iata)



