from src.data_store import data_store
from src.error import AccessError
import hashlib
import jwt

SECRET = 'H09BELEPHANT'
SESSION_TRACKER = 0


def hash(password):
    hashed_pword = hashlib.sha256(str(password).encode()).hexdigest()

    return hashed_pword


def generate_token(user_id):
    store = data_store.get()
    session_id = generate_session_id()
    ENCODED_JWT = jwt.encode(
        {'u_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

    store['session_list'].append(hash(session_id))
    data_store.set(store)

    return ENCODED_JWT


def generate_session_id():
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER


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

    store = data_store.get()
    print(token_decoded)
    if hash(token_decoded['session_id']) in store['session_list']:
        return token_decoded
    else:
        raise AccessError(description="Invalid session_id")
