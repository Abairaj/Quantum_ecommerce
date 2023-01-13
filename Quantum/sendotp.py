from django.conf import settings
from twilio.rest import Client
import random
from twilio.http.http_client import TwilioHttpClient
import os







# proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

# account_sid = settings.TWILIO_ACCOUNT_SID
# auth_token = settings.TWILIO_AUTH_TOKEN


# class MessageHandler:

#     phone_number = None
#     otp = None


#     def __init__(self,phone_number,otp):
#         self.phone_number = phone_number
#         self.otp = otp

#     def send_otp(self):
#         client = Client(account_sid, auth_token, http_client=proxy_client)
#         message = client.messages.create(
#             body = f'Your otp is {self.otp}',
#             from_ = '+18608548553',
#             to = '+91'+str(self.phone_number)

#         )



def send_otp(mobile,otp):

    # proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    # twilio api calls will now work from behind the proxy:
    message = client.messages.create(
                    body = f'Your otp is {otp}',
            from_ = '+18608548553',
            to = '+91'+str(mobile)
    )

 