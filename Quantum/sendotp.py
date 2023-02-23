from django.conf import settings
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient



def send_otp(mobile,otp):


    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)


    message = client.messages.create(
                    body = f'Your Quantum Times otp is {otp}',
            from_ = '+18608548553',
            to = '+91'+str(mobile)
    )

 