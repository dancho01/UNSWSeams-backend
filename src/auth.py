import re
from src.data_store import data_store
from src.error import InputError
from src.auth_helper import generate_new_jwt, encrypt_password, generate_new_session_id, generate_new_handle

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
    
    # converts plaintext password to its hashed form 
    encrypted_pw = encrypt_password(password)

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
            if user['password'] != encrypted_pw:
                raise InputError("Incorrect Password!")
            else:
                # generate new session_id to add to user's session_list 
                session_id = generate_new_session_id()                           
                user['session_list'].append(session_id)
                
                data_store.set(store)
                
                return {'auth_user_id': user['auth_user_id'],
                        'token': generate_new_jwt(user['handle'], session_id)
                }


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
        InputError      - Occurs when length of name_first is not between 1 and 50
                        characters inclusive
        InputError      - Occurs when length of name_last is not between 1 and 50 
                        characters inclusive

    Return Value:
        Returns a dictionary with the key 'auth_user_id', which is an integer value, if
        account is successfully created
    '''
    store = data_store.get()

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
    final_handle = generate_new_handle(name_first, name_last, store)
    
    # associating global permissions to user_id
    if new_id == 1:
        perms = 1
    else:
        perms = 2
     
    # converts the plaintext password to its hashed form    
    encrypted_pw = encrypt_password(password)    

    # adding all information to dictionary
    new_user = {'auth_user_id': new_id, 'name_first': name_first, 'name_last': name_last,
                'email': email, 'password': encrypted_pw, 'handle': final_handle, 'global_permissions': perms
                , 'session_list':[]}
                
    # generate new session_id to add to user's session_list 
    session_id = generate_new_session_id()               
    new_user['session_list'].append(session_id)
        
    store['users'].append(new_user)

    data_store.set(store)

    return {
        'auth_user_id': new_id,
        'token': generate_new_jwt(final_handle, session_id)
    }

