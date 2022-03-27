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

# YOU SHOULD MODIFY THIS OBJECT BELOW

initial_object = {
    'users': [],
    'channels': [],
    'dms': [],
    'session_list': []
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
            'handle' : ''
        },
        {
            'auth_user_id': 2,
            'name': 'user2',
            'global_permissions': 2,
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
}
'''
