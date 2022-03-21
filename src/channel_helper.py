from src.error import InputError, AccessError


def check_message(message):
    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            message='length of message is less than 1 or over 1000 characters')
