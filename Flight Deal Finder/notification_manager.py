from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ["ACCOUNT_SID"]
        self.auth_token = os.environ["AUTH_TOKEN"]
        self.virtual_number = os.environ["VIRTUAL_NUMBER"]
        self.my_number = os.environ["MY_NUMBER"]

    def send_message(self, lowest_price, origin, destination, out_date, return_date):
        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
            from_=self.virtual_number,
            body=f"Low price alert! Only £{lowest_price} to fly from {origin} to {destination}, on {out_date} "
                 f"until {return_date} ",
            to=self.my_number
        )

        print(message.sid)

        # Is SMS not working for you or prefer whatsapp? Connect to the WhatsApp Sandbox!
        # https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

    # def send_whatsapp(self, message_body):
    #     message = self.client.messages.create(
    #         from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
    #         body=message_body,
    #         to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
    #     )
    #     print(message.sid)
