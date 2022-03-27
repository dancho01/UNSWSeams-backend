from src.data_store import data_store
from src.error import AccessError
import hashlib
import jwt

SECRET = 'H09BELEPHANT'


def hash(password):
    hashed_pword = hashlib.sha256(str(password).encode()).hexdigest()

    return hashed_pword


def generate_token(user_id, handle):
    store = data_store.get()
    session_id = generate_session_id(user_id, handle)
    ENCODED_JWT = jwt.encode(
        {'u_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

    store['session_list'].append(session_id)

    return ENCODED_JWT


def generate_session_id(user_id, handle):
    return (hash(str(user_id) + handle))


def check_valid_token(token):
    '''
    Decodes the jwt string back into the user's data that was stored
    Args:
        hashed_jwt      str         the JWT string containing the header, payload and signature
    Return:
        Returns an object storing the user's data that was used to generate the JWT
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
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id and user['active']:
            return

    raise AccessError(
        description="u_id from token does not match a valid user")
