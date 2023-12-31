from datetime import datetime, timezone


'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''


def time_now():
    '''
    returns the current time stamp
    '''
    return int(datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp())

# YOU SHOULD MODIFY THIS OBJECT BELOW


initial_object = {
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
# YOU SHOULD MODIFY THIS OBJECT ABOVE

# YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH


class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


print('Loading Datastore...')

global data_store
data_store = Datastore()


'''
Example of what the data structure look like
'''

'''
data = {
    'users': [
        {
            'auth_user_id': 1,
            'name': 'user1',
            'global_permissions': 1,
            'handle' : '',
            'stats': {
                'user_stats': {
                    'channels_joined': [
                        {
                            'num_channels_joined': 0,
                            'time_stamp': 0
                        }, 
                        {
                            'num_channels_joined': 1,
                            'time_stamp': 23456789
                        }
                    ],
                    'dms_joined': [
                        {
                            'num_dms_joined': 0,
                            'time_stamp': 0
                        },
                        {
                            'num_dms_joined': 1,
                            'time_stamp': 987654
                        }
                    ],
                    'messages_sent': [
                        {
                            'num_msgs_sent': 0,
                            'time_stamp': 0
                        }, 
                        {
                            'num_msgs_sent': 1,
                            'time_stamp': 1234590
                        }
                    ],
                    'involvement_rate': 0.0
                },
                "total_channels_joined": 1,
                "total_dms_joined": 1,
                "total_messages_sent": 1
            }
        },
        {
            'auth_user_id': 2,
            'name': 'user2',
            'global_permissions': 2,
            'stats': {
                'user_stats': {
                    'channels_joined': [
                        {
                            'num_channels_joined': 0,
                            'time_stamp': 0
                        }, 
                        {
                            'num_channels_joined': 1,
                            'time_stamp': 23456789
                        }
                    ],
                    'dms_joined': [
                        {
                            'num_dms_joined': 0,
                            'time_stamp': 0
                        },
                        {
                            'num_dms_joined': 1,
                            'time_stamp': 987654
                        }
                    ],
                    'messages_sent': [
                        {
                            'num_msgs_sent': 0,
                            'time_stamp': 0
                        }, 
                        {
                            'num_msgs_sent': 1,
                            'time_stamp': 1234590
                        }
                    ],
                    'involvement_rate': 0.0
                }, 
                "total_channels_joined": 0,
                "total_dms_joined": 0,
                "total_messages_sent": 0
            }
        },
    ],
    'channels': [
        {
            'channel_id': 1,
            'name': 'channel1',
            'all_members': [{'email': 'user1@example.com'}], #authorized member ids (if its private)
            'owner_members' : [1, 2, 3]  #user_id for admins
            'is_public': False,
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 4132,
                },
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 2313,
                },
            ],
        },
    ],
    'session_list': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxLCJzZXNzaW9uX2lkIjoxfQ.28WKin5WZMLred8_JiUtse4O4BZCvB5AQXRehRrWrHU'],
    'dms': [{'dm_id': new_dm_id,
              'name': name,
              'all_members': [],
              'messages': [],
            ],
    'workspace_stats': {
        'channels_exist': [
            {
                'num_channels_exist': 0,
                'time_stamp': 0
            }, 
            {
                'num_channels_exist': 1,
                'time_stamp': 23456789
            }
        ],
        'dms_exist': [
            {
                'num_dms_exist': 0,
                'time_stamp': 0
            },
            {
                'num_dms_exist': 1,
                'time_stamp': 987654
            }
        ],
        'messages_exist': [
            {
                'num_messages_exist': 0,
                'time_stamp': 0
            }, 
            {
                'num_messages_exist': 1,
                'time_stamp': 1234590
            }
        ],
        'utilization_rate': 0.0
    }
}
'''
