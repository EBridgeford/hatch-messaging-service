
import random

from fastapi import Response, status
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed

from app.schemas.messages import Message


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def send_email(msg: Message) -> Response:
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
