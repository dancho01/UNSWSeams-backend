from src.error import InputError
from src.data_store import data_store
from src.token import hash
from flask_mail import Message
import re
import random


def generate_new_handle(name_first, name_last, store):
    '''
    Generates a unique handle for the recently registered user based 
    on user's first and last name, if a users active key is false, then 
    it will be able to reuse that specific handle.
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
    '''
        Every user is checked for whether their user['active'] key
        is True, true means user has not being removed whereas
        false means they have been removed
    '''
    if user['name_first'] == "Removed" and user['name_last'] == "user":
        return True
    else:
        return False


def check_info_syntax(name_first, name_last, password, email):
    '''
        Checks the syntax of first name, lastname, password and checks
        whether email exists and if the format of the email is legit
    '''
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            description="First name must be between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            description="Last name must be between 1 and 50 characters inclusive")

    if len(password) < 6:
        raise InputError(description="Password must be 6 or more characters!")

    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}$", email):
        raise InputError(description="Invalid email!")

    store = data_store.get()

    for user in store['users']:
        if user['email'] == email and is_user_removed(user) == False:
            raise InputError(
                description="This email is already in use by another user!")

    return


def check_login(email, password):
    '''
        Checks if the email is in the database, then checks if the
        hashed password that is inputted matches
    '''
    store = data_store.get()

    for user in store['users']:
        if user['email'] == email:
            if user['password'] == hash(password):
                print(user['password'])
                print(hash(password))
                return {'u_id': user['auth_user_id'],
                        'handle': user['handle']}
            else:
                raise InputError(description="Incorrect Password!")

    raise InputError(description="This email is not registered!")


def assign_permissions():
    '''
        Sees how many users there are by looking at length of store['users],
        if the length is 0 then this means the user being registered is
        the first user on the server, giving them global permissions
    '''
    store = data_store.get()

    if len(store['users']) == 0:
        return 1
    else:
        return 2
    
def check_email_exist(email):
    ''' 
        iterates through data store and returns the UID corresponding to
        the users email
    '''

    store = data_store.get()

    for user in store['users']:
        if user['email'] == email:
            return user['auth_user_id']

    return ""

def generate_reset_code(uid):
    '''
        appends a dictionary containing a reset code and the user which
        ordered the reset to the data store

    '''

    store = data_store.get()

    code = random.randint(1000,9999)
    
    print("in generate function")
    
    # case: code already exists
    #if store['reset_codes']: # so that we don't iterate through an empty list
    for codes in store['reset_codes']:
        if codes['code'] == code: # if the code already exists in the datastore, create a different one
            generate_reset_code(uid)
            
    store['reset_codes'].append({'uid': uid,
                                 'code': code})
    
    return code 


def email_reset_code(email, code, mail):
    '''
        takes in an email, the pin code and mail object created in server.py
        sends the reset email to user
    '''
    msg = Message('Your Seams Reset Code', sender = 'h09belephant@gmail.com', recipients = [email])
    msg.body = str(code)
    mail.send(msg) 
    return
    

