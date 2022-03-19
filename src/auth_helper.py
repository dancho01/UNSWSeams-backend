import jwt
import hashlib

SECRET = 'SecretStringOnlyIKnow'
SESSION_ID_COUNTER = 0


def generate_new_jwt(handle, session_id):
    '''
    Generates a new JWT based on the user's handle, session_id and the SECRET global string
    Args: 
        handle          str         the user's unique handle
        session_id      int         the session_id generated upon logging in or registering
        
    Return:
        Returns the JWT that is a tamper-proof encoded string containing the information about the user in the payload
    '''
    return jwt.encode({'handle': handle, 'session_id': session_id}, SECRET, algorithm='HS256')
    
    
def encrypt_password(plaintext_pw):
    '''
    Using the sha256 algorithm, takes the plaintext password and encrypts it 
    Args:
        plaintext_pw    str         the user's password in plaintext form
    
    Return:
        Returns the encrypted password, formatted in hexidigest 
    '''
    return hashlib.sha256(plaintext_pw.encode()).hexdigest()
    
    
def generate_new_session_id():
    '''
    Generates a new session_id that is sequentially increasing by 1
    Args:
        None
    Return:
        Returns the next session id
    '''
    global SESSION_ID_COUNTER
    SESSION_ID_COUNTER += 1
    return SESSION_ID_COUNTER
    
    
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
        if user['handle'] == final_handle:
            final_handle = handle + str(count)
            count += 1
            
    return final_handle
    
    
