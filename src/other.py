from src.data_store import data_store
import src.global_helper

global AUTH_COUNTER
global CHANNEL_COUNTER
AUTH_COUNTER = 0
CHANNEL_COUNTER = 0

def clear_v1():
    store = data_store.get()

    store = {
        'users': [],
        'channels': [],
        'dms': [],
        'session_list': [],
    }

    data_store.set(store)

    return {}
