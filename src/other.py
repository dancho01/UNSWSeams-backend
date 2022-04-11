from src.data_store import data_store
from src.global_helper import reset_globals
from src.channel_helper import time_now

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
        'stats': {
        'workspace_stats':{
            'channels_exist': [
                {
                    'num_channels_exist': 0,
                    'time_stamp': time_now()
                }
            ],
            'dms_exist': [
                {
                    'num_dms_exist': 0,
                    'time_stamp': time_now()
                }
            ],
            'messages_exist': [
                {
                    'num_messages_exist': 0,
                    'time_stamp': time_now()
                }
            ],
            'utilization_rate': 0.0
        },
        'total_num_channels': 0,
        'total_num_dms': 0,
        'total_num_messages': 0
        },
        'reset_codes':[]
    }

    data_store.set(store)

    return {}
