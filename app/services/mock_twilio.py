# https://www.twilio.com/docs/messaging/api/message-resource#create-a-message-resource
# Based on
#
# {
#  "ApplicationSid": "APaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
#  "Body": "Hello! 👍",
#  "From": "+14155552345",
#  "MediaUrl": [
#    "https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg"
#  ],
#  "PersistentAction": [
#    "mailto:test@example.com"
#  ],
#  "StatusCallback": "https://example.com",
#  "To": "+14155552345",
#  "Tags": "{\"campaign_name\": \"Spring Sale 2022\",\"message_type\": \"cart_abandoned\"}"
# }

import random

from fastapi import Response, status
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed

from app.schemas.messages import Message


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def send_sms(msg: Message) -> Response:
    # Assume that a provider may return HTTP error codes like 500, 429 and plan accordingly
    status_codes = [
        status.HTTP_200_OK,
        #status.HTTP_400_BAD_REQUEST,
        #status.HTTP_429_TOO_MANY_REQUESTS,
        #status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    status_choice = random.choice(status_codes)

    if status_choice != status.HTTP_200_OK:
        print("Non-200 HTTP code from the sms service, retrying")
        raise Exception("Bad result, retry")

    response = Response()
    response.status_code = status_choice
    return response
