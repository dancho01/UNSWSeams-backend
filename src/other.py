from src.data_store import data_store


def clear_v1():
    store = data_store.get()

    store = {
        'users': [],
        'channels': [],
        'session_list': []
    }

    data_store.set(store)

    return {}
