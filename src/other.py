from src.data_store import data_store
import data

def clear_v1():
    
    data.data = {
        'users' : [],
        'channels' : []
    }
    
    return {}
