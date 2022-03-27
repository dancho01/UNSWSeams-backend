from src.data_store import data_store
from src.global_helper import reset_globals


def clear_v1():
    '''
        Calls reset_globals which resets all global variables in
        global_helper.py, also resets the datastruct to its 
        original form
    '''
    store = data_store.get()
    reset_globals()
    store = {
        'users': [],
        'channels': [],
        'dms': [],
        'session_list': [],
    }

    data_store.set(store)

    return {}
