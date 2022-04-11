import pickle
from src.global_helper import load_globals, get_globals
from src.data_store import data_store
from src.user_helper import clear_profile_images


def save_data():
    store = data_store.get()
    auth_counter, channel_counter, message_counter = get_globals()
    # global AUTH_COUNTER, CHANNEL_COUNTER
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(
            [store, auth_counter, channel_counter, message_counter], FILE)


def load_data():
    try:
        # global AUTH_COUNTER, CHANNEL_COUNTER
        # opens locally stored pickle file
        data, auth_counter, channel_counter, message_counter = pickle.load(
            open("data_store.p", "rb"))
        # inserts it into the data_store datastruct
        load_globals(auth_counter, channel_counter, message_counter)
        data_store.set(data)
    except Exception:
        # if file cannot be opened datastructure is returned to original state
        data_store.__init__
        clear_profile_images()
