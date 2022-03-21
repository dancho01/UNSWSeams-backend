from src.data_store import data_store


def clear_v1():
    store = data_store.get()

    store = {
        'users': [],
        'channels': [],
<<<<<<< HEAD
        'session_list': []
=======
        'dms': [],
        'session_list': [],
>>>>>>> cadb01d1f93e27fe7e40f9a5208d122a60d6637c
    }

    data_store.set(store)

    return {}
