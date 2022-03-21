from src.error import InputError, AccessError
from datetime import datetime, timezone


def check_message(message):
    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='length of message is less than 1 or over 1000 characters')


def time_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
