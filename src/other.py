from src.data_store import data_store


def clear_v1():
    store = data_store.get()

    store = {
        'users': [],
        'channels': [],
<<<<<<< HEAD
        'dms': [],
        'session_list': [],
=======
        'session_list': []
>>>>>>> dad99a26cff97beb455d807e7643f1352e7433c5
    }

    data_store.set(store)

    return {}
