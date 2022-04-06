from src.data_store import data_store
from src.error import AccessError
from src.channel_helper import time_now
import hashlib
import jwt

SECRET = 'H09BELEPHANT'


def hash(password):
    '''
        Hashes the input with sha256
    '''
    hashed_pword = hashlib.sha256(str(password).encode()).hexdigest()

    return hashed_pword


def generate_token(user_id, handle):
    '''
        Takes the session_id from generate_session_id and the user_id,
        places it into the token and encodes it as a JWT
    '''
    store = data_store.get()
    time_logged = time_now()
    session_id = generate_session_id(user_id, handle, time_logged)

    ENCODED_JWT = jwt.encode(
        {'u_id': user_id, 'session_id': session_id, 'time_logged': time_logged}, SECRET, algorithm='HS256')

    store['session_list'].append(session_id)

    return ENCODED_JWT


def generate_session_id(user_id, handle, time_logged):
    '''
        Hashes the concatenation of user_id and handle, uses
        it as the session_id
    '''
    return (hash(str(user_id) + handle + str(time_logged)))


def check_valid_token(token):
    '''
        Tries to check if it is a valid token that can be decoded, if 
        not then error is raised. 

        Then calls validate_token_u_id which matches the users id with
        an id in the database

        Finally, it checks to see if this user is currently in the 
        session_list.
    '''

    try:
        token_decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    except Exception as error:
        raise AccessError(description="Invalid Token") from error

    validate_token_u_id(token_decoded['u_id'])

    store = data_store.get()
    if token_decoded['session_id'] in store['session_list']:
        return token_decoded
    else:
        raise AccessError(description="Invalid session_id")


def validate_token_u_id(u_id):
    '''
        Checks if u_id exists in the database
    '''
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id and user['active']:
            return

    raise AccessError(
        description="u_id from token does not match a valid user")
