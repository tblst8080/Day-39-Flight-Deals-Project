import requests
from twilio.rest import Client
from email.mime.text import MIMEText
import smtplib

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self):
        self.recipient = '+12563304532'
        self.sender = "+13128209309"

        self.e_recipient = "germsandspices@yahoo.com"
        self.e_sender = "germsandspices@gmail.com"
        self.password = "mrkhdjilpjdhlgmg"

        # Access Twilio Account
        self.client = Client('AC7ed8990511c2f7540a17ddf1e0b78934', '98ddc2370619d08946b18e23a811d403')

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

    def send_email(self, catalog:list):  # TODO: Email each subscriber flights corresponding to their departure city
        """Generate message for each flight from the catalog, and sends email notification via SMTP"""
        if len(catalog) == 0:
            # Generate message:
            message = f"Subject: No good prices found."

            # Send email
            with smtplib.SMTP('smtp.gmail.com') as connection:
                print(1)
                connection.starttls()
                print(2)
                connection.login(user = self.e_sender, password=self.password)
                print(3)
                connection.sendmail(from_addr=self.e_sender, to_addrs=self.e_recipient, msg=message)
        else:
            email_body = ""
            for flight in catalog:
                email_body += f"""\n<pre> 
                <b>Flight from {flight['f_city']}({flight['f_airport']}) to {flight['t_city']}({flight['t_airport']}) for ${flight['price']}</b>\n
                From {flight['departure'].strftime("%m/%d/%Y")} to {flight['return'].strftime("%m/%d%Y")}\n
                <a href="{flight['link']}">Click here to book flight!</a>
                </pre>"""

            msg = MIMEText(email_body, 'html')

            msg['Subject'] = f"Low Price Alert!"
            msg['From'] = 'xxx'
            msg['To'] = 'Subscribers'

            with smtplib.SMTP('smtp.gmail.com') as connection:
                print(1)
                connection.starttls()
                print(2)
                connection.login(user=self.e_sender, password=self.password)
                print(3)
                connection.sendmail(from_addr=self.e_sender, to_addrs=self.e_recipient, msg=msg.as_string())
