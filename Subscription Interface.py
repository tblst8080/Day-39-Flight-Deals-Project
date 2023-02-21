import requests
from tequilaAPI import FlightSearch
from sheetyAPI import Subscriber

print("Welcome to the Flight Club")

print('We find the best flgiht deals and email you.')

first_name = input("Please enter your first name: \n").title()

last_name = input("Please enter your last name: \n").title()

email = input("Please enter your email: \n")

origin = input("What city do you wish to depart from? \n").title()


my_searcher = FlightSearch()

iata = my_searcher.find_code(origin)

my_uploader = Subscriber()
my_uploader.add_user(first_name = first_name, last_name=last_name, email=email, origin=origin, iata=iata)


