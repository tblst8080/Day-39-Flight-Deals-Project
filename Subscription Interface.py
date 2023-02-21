from tequilaAPI import FlightSearch
from sheetyAPI import Subscriber
from sms_smtp import NotificationManager
import os

def clear_terminal():
  os.system('cls' if os.name == 'nt' else 'clear')

def check_origin(message):
    origin = input(message).title()
    code = my_searcher.find_code(origin)
    if not code:
        clear_terminal()
        return check_origin("Invalid city name. Please enter another one: \n")
    else:
        return code, origin

def ask_email():

    email = input("Please enter your email: \n")
    if not my_uploader.add_user(first_name=first_name, last_name=last_name, email=email, origin=origin, iata=iata):
        clear_terminal()
        print("Email is already in the system. Please enter another one.")
        return ask_email()
    else:
        if not my_notifier.verify(email=email):
            clear_terminal()
            print("Email invalid. Please try another one.")
            return ask_email()
        else:
            return

my_searcher = FlightSearch()
my_uploader = Subscriber()
my_notifier = NotificationManager()

print("Welcome to the Flight Club")
print('We find the best flight deals and email you.')
first_name = input("Please enter your first name: \n").title()
last_name = input("Please enter your last name: \n").title()
iata, origin = check_origin("What city do you wish to depart from? \n")

ask_email()

clear_terminal()

print("Your info has been added to the system!")




