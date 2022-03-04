import re
from src.data_store import data_store
from src.error import InputError


def auth_login_v1(email, password):
    store = data_store.get()

    found = False
    for user in store['users']:
        if user['email'] == email:
            found = True

    if found != True:
        raise InputError("This email is not registered!")

    for user in store['users']:
        if user['email'] == email:
            if user['password'] != password:
                raise InputError("Incorrect Password!")
            else:
                return {'auth_user_id': user['auth_user_id']}


def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()

    ## according to the handle spec, alphanumeric + specials are allowed in names
    # if not name_first.isalpha():
    #     raise InputError(
    #         "Special characters / numbers are not allowed in the name!")

    # if not name_last.isalpha():
    #     raise InputError(
    #         "Special characters / numbers are not allowed in the name!")

    if len(name_first) < 1:
        raise InputError("Input a first name!")

    if len(name_first) > 50:
        raise InputError(
            "Input a first name less than or equal to 50 characters!")

    if len(name_last) < 1:
        raise InputError("Input a last name!")

    if len(name_last) > 50:
        raise InputError(
            "Input a last name less than or equal to 50 characters!")

    if len(password) < 6:
        raise InputError("Password must be 6 or more characters!")
        
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise InputError("Invalid email!")

    for user in store['users']:
        if user['email'] == email:
            raise InputError("This email is already in use by another user!")

    # creates a new id depending on how many users exist
    new_id = len(store['users']) + 1

    # creating handle from first and last name
    name = name_first + name_last
    handle = ""
    for char in name:
        if char.isalnum():
            handle += char.lower()
    
    handle = handle[0:20]
    count = 0
    for user in store['users']:
        if user['handle'] == handle:
            handle += str(count)
            count += 1

    # associating channel permissions to user_id
    if new_id == 1:
        perms = 1
    else:
        perms = 2

    # adding all information to dictionary 
    new_user = {'auth_user_id': new_id, 'name': name_first + ' ' +
            name_last, 'email': email, 'password': password, 'handle': handle, 
            'global_permissions': perms}

    store['users'].append(new_user)

    data_store.set(store)
    
    return {
        'auth_user_id': new_id,
    }
