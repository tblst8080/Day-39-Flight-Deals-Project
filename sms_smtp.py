import requests
from twilio.rest import Client
from email.mime.text import MIMEText
from APIs import sender_number, recipient_number, twilio_sid, twilio_token, sender_email, sender_password
import smtplib

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self):
        self.recipient = recipient_number
        self.sender = sender_number

        self.e_sender = sender_email
        self.password = sender_password

        # Access Twilio Account
        self.client = Client(twilio_sid, twilio_token)

    def send_sms(self, catalog:list):
        """Generates notification from each entry of FlightData catalog and sends it via Twilio SMS"""
        for flight in catalog:
            # generate message:
            message = f"Low Price Alert!\nRound trip flight from {flight['f_city']}({flight['f_airport']}) to {flight['t_city']}({flight['t_airport']}) from {flight['departure'].date()} to {flight['return'].date()} for ${flight['price']}!"
            print(message)

            # Send SMS
            my_sms = self.client.messages \
                .create(
                body=message,
                from_=self.sender,
                to=self.recipient
            )

            print(my_sms.status)

    def send_email(self, catalog:dict, subscription_list:list):
        """Generate message for each flight from the catalog, and sends email notification via SMTP"""
        for subscriber in subscription_list:
            recipient = subscriber['email']
            first_name = subscriber['firstName']
            last_name = subscriber['lastName']

            if subscriber['iataCode'] in [item[0] for item in catalog.keys()]:
                email_body = f"""
        <p style="font-family:'Times New Roman';font-size:14px"><b>Hello {first_name} {last_name}!</b></br></p>"""


                for key, value in catalog.items():
                    if subscriber['iataCode'] == key[0]:
                        for flight in value:
                            if flight.stopover > 0:
                                stopover_msg = f"Flight has {flight.stopover} stopover via {flight.via_city}.<br>"
                            else:
                                stopover_msg = "Direct flight.<br>"

                            email_body += f"""
        \n<p style="font-family:'Times New Roman';font-size:14px"><b>✈ Flight from {flight.cityFrom}({flight.airportFrom}) to {flight.cityTo}({flight.airportTo}) for ${flight.price}!</b><br>
        {stopover_msg}
        From {flight.departure_flight.strftime("%m/%d")} to {flight.return_flight.strftime("%m/%d")}<br>
        <a href="{flight.link}">Click here to book flight!</a><br><br>
        </p>"""

                msg = MIMEText(email_body, 'html')

                msg['Subject'] = f"Low Price Alert!"
                msg['To'] = 'Subscribers'
                with smtplib.SMTP('smtp.gmail.com') as connection:
                    connection.starttls()
                    connection.login(user=self.e_sender, password=self.password)
                    connection.sendmail(from_addr=self.e_sender, to_addrs=recipient, msg=msg.as_string())

            else:
                # Generate message:
                message = f"Subject: No good prices found."

                # Send email
                with smtplib.SMTP('smtp.gmail.com') as connection:
                    connection.starttls()
                    connection.login(user=self.e_sender, password=self.password)
                    connection.sendmail(from_addr=self.e_sender, to_addrs=recipient, msg=message)
