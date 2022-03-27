from src.error import InputError, AccessError
from src.data_store import data_store
import re


def generate_new_handle(name_first, name_last, store):
    '''
    Generates a unique handle for the recently registered user based on user's first and last name 
    Args:
        name_first      str         user's first name
        name_last       str         user's last name
        store           dict        copy of the data structure in data_store
    Return:
        Returns the final handle that is concatenated such that it is unique    
    '''
    name = name_first + name_last
    handle = ""
    for char in name:
        if char.isalnum():
            handle += char.lower()

    # if concatenated handle is longer than 20 characters, it is cut off at length of 20
    if len(handle) > 20:
        handle = handle[0:20]

    count = 0
    final_handle = handle
    # iterates through list of users to check if handle is already taken
    for user in store['users']:
        if user['handle'] == final_handle and not is_user_removed(user):
            final_handle = handle + str(count)
            count += 1

    return final_handle


def is_user_removed(user):
    if user['name_first'] == "Removed" and user['name_last'] == "user":
        return True
    else:
        return False


def check_info(name_first, name_last, password, email):

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            description="First name must be between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            description="Last name must be between 1 and 50 characters inclusive")

    if len(password) < 6:
        raise InputError(description="Password must be 6 or more characters!")

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise InputError(description="Invalid email!")

    store = data_store.get()

    for user in store['users']:
        if user['email'] == email and is_user_removed(user) == False:
            print("------------------------------------------------------------")
            print(is_user_removed(user))
            raise InputError(
                description="This email is already in use by another user!")

    return
