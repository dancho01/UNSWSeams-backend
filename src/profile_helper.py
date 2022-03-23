from ast import In
import re
from src.error import AccessError, InputError
from src.data_store import data_store


def check_name(name_first, name_last):

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            description="First name must be between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            description="Last name must be between 1 and 50 characters inclusive")

    return


def check_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise InputError(description="Invalid email!")

    store = data_store.get()

    for user in store['users']:
        if user['email'] == email:
            raise InputError(
                description="This email is already in use by another user!")


def check_handle(handle):

    if len(handle) < 3 or len(handle) > 20:
        raise InputError(
            description="length of handle_str is not between 3 and 20 characters inclusive")

    if not handle.isalnum():
        raise InputError(
            description="handle_str contains characters that are not alphanumeric")

    store = data_store.get()

    for user in store['users']:
        if user['handle'] == handle:
            raise InputError(
                description="the handle is already used by another user")
