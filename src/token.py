import hashlib
import jwt

SECRET = 'H09BELEPHANT'
SESSION_TRACKER = 0


def hash(password):
    hashed_pword = hashlib.sha256(str(password).encode()).hexdigest()

    return hashed_pword


def generate_token(user_id):
    session_id = generate_session_id()
    ENCODED_JWT = jwt.encode(
        {'u_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

    return ENCODED_JWT


def generate_session_id():
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return hash(SESSION_TRACKER)
