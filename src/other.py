from src.data_store import data_store
import data_store

def clear_v1():
    
    data_store.data = {
        'users' : [],
        'channels' : []
    }
    
    return {}
