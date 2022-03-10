import re
from src.data_store import data_store
from src.error import InputError


def auth_login_v1(email, password):
    '''
    This function logs in a registered user, given their email and password
    Arguments:
        email         string         - the registered user's email
        password      string         - the registered user's password

    Exceptions:
        InputError      - Occurs when email entered does not belong to a user
        InputError      - Occurs when password is not correct 

    Return Value:
        Returns a dictionary with the key 'auth_user_id', an integer value, if
        login is successful
    '''
    store = data_store.get()

    # iterates through users to check if email belongs to a user
    found = False
    for user in store['users']:
        if user['email'] == email:
            found = True

    # InputError is raised if valid email is not found
    if found != True:
        raise InputError("This email is not registered!")

    for user in store['users']:
        if user['email'] == email:
            # InputError is raised if password does not match
            if user['password'] != password:
                raise InputError("Incorrect Password!")
            else:
                return {'auth_user_id': user['auth_user_id']}


def auth_register_v1(email, password, name_first, name_last):
    '''   
    This function registers a user, given the input of their first name, last name,
    email address and password, creating a new account for them. It is also responsible
    for generating the handle for the user. The handle must be unique for each user,
    so if a handle generated already exists, then a number is appended to it until
    it is unique.

    Arguments:
        email           string         - the user's email they want to register with
        password        string         - the user's intended password to use
        name_first      string         - the user's first name
        name_last       string         - the user's last name

    Exceptions:
        InputError      - Occurs when email entered is not a valid channel
        InputError      - Occurs when email address is already being used by another user
        InputError      - Occurs when length of password is less than 6 characters
        InputError      - Occurs when length of name_first is not between 1 and 50 characters inclusive
        InputError      - Occurs when length of name_last is not between 1 and 50 characters inclusive

    Return Value:
        Returns a dictionary with the key 'auth_user_id', which is an integer value, if
        account is successfully created
    '''
    store = data_store.get()

    # according to the handle spec, alphanumeric + specials are allowed in names
    # if not name_first.isalpha():
    #     raise InputError(
    #         "Special characters / numbers are not allowed in the name!")

    # if not name_last.isalpha():
    #     raise InputError(
    #         "Special characters / numbers are not allowed in the name!")

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            "First name must be between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            "Last name must be between 1 and 50 characters inclusive")

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

    # if concatenated handle is longer than 20 characters, it is cut off at length of 20
    if len(handle) > 20:
        handle = handle[0:20]

    count = 0
    final_handle = handle
    # iterates through list of users to check if handle is already taken
    for user in store['users']:
        if user['handle'] == final_handle:
            final_handle = handle + str(count)
            count += 1

    # associating channel permissions to user_id
    if new_id == 1:
        perms = 1
    else:
        perms = 2

    # adding all information to dictionary
    new_user = {'auth_user_id': new_id, 'name_first': name_first, 'name_last': name_last,
                'email': email, 'password': password, 'handle': final_handle, 'global_permissions': perms}

    store['users'].append(new_user)

    data_store.set(store)

    return {
        'auth_user_id': new_id,
    }
