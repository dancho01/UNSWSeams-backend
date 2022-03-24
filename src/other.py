from src.data_store import data_store
from src.global_helper import reset_globals


def clear_v1():
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
