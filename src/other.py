from src.data_store import data_store
from src.global_helper import reset_globals
from src.channel_helper import time_now
from src.user_helper import clear_profile_images


def clear_v1():
    '''
        Calls reset_globals which resets all global variables in
        global_helper.py, also resets the datastruct to its 
        original form
    '''
    store = data_store.get()
    reset_globals()
    store = {
        'users': [{'auth_user_id': - 1,
                   'name_first': 'Seams',
                   'name_last': 'Bot',
                   'email': 'seams_admin@gmail.com',
                   'password': hash('iamrobot'),
                   'handle': 'seamsbot',
                   'global_permissions': 2,
                   'active': True,
                   'notifications': [],
                   'stats': {
                       'user_stats': {
                           "channels_joined": [
                               {
                                   "num_channels_joined": 0,
                                   "time_stamp": time_now()
                               }
                           ],
                           "dms_joined": [
                               {
                                   "num_dms_joined": 0,
                                   "time_stamp": time_now()
                               }
                           ],
                           "messages_sent": [
                               {
                                   "num_messages_sent": 0,
                                   "time_stamp": time_now()
                               }
                           ],
                           "involvement_rate": 0.0
                       },
                       "total_channels_joined": 0,
                       "total_dms_joined": 0,
                       "total_messages_sent": 0
                   },
                   'profile_img_url': 'https://pacetoday.com.au/wp-content/uploads/2016/02/Applications-robot.jpg'}],
        'channels': [],
        'dms': [],
        'session_list': [],
        'stats': {
            'workspace_stats': {
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
        'reset_codes': []
    }
    clear_profile_images()

    data_store.set(store)

    return {}
