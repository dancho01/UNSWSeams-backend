import pickle
import src.global_helper
from src.data_store import data_store


def save_data():
    store = data_store.get()
    # global AUTH_COUNTER, CHANNEL_COUNTER
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(store, FILE)


def load_data():
    try:
        # global AUTH_COUNTER, CHANNEL_COUNTER
        # opens locally stored pickle file
        data = pickle.load(
            open("data_store.p", "rb"))
        # inserts it into the data_store datastruct
        data_store.set(data)
    except Exception:
        # if file cannot be opened datastructure is returned to original state
        data_store.__init__
