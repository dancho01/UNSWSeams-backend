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


def check_valid_channel(channel_id, data_store):
    '''
    check_valid_channel goes through data_stores['channels']['index']['channel_id'] which includes the name
    of every single channel that is created within the data structure, if there is a match then True is returned
    else False is returned.

    Arguments:
        channel_id      int         - id of the channel that is to be searched
        data_store      dict        - copy of the datastructure

    Return Value:
        Returns True if channel_id matches with any channels within the datastructure
        Returns channel_index when a match is found, this way the channel does not have to be found again
                saving resources
        Returns False if Channel_id is not found
    '''

    channel_list = data_store['channels']

    for channel_index in range(len(channel_list)):
        if channel_list[channel_index]['channel_id'] == channel_id:
            return True, channel_index

    return False


def check_authorization(auth_user_id, index, data_store):
    '''
    check_authorization works in tandem with check_valid_channel, it takes the outputted index if
    check_valid_channel returns a True. It uses that index to access the 'all_members' list where
    if the user is apart of all_members, it will return True else return False.

    Arguments:
        auth_user_id    int         - id of the user that is to be searched
        index           int         - Index of the channel that is to be searched
        data_store      dict        - copy of the datastructure   

    Return Value:
        Returns True if user in channels ['all_members'] list
        Returns False if user not in channels ['all_members'] list
    '''
    channel_authorization = data_store['channels'][index]['all_members']
    for user_index in range(len(channel_authorization)):
        if channel_authorization[user_index]['u_id'] == auth_user_id:
            return True

    return False


def check_user_registered(auth_user_id, data_store):
    '''
    check_user_registered loops through data_store['users]['auth_user_id] of each element within
    all the users, it returns true if the user is stored but will return false if the user is 
    not stored.

    Arguments:
        auth_user_id    int         - id of the user that is to be searched
        data_store      dict        - copy of the datastructure   

    Return Value:
        Returns True if a match is found for auth_user_id
        Returns False if a match is not found for auth_user_id
    '''
    user_list = data_store['users']

    for user in user_list:
        if user['auth_user_id'] == auth_user_id:
            return True

    return False


def messages_returned(channel_index, start, end, store):
    '''
    messages_returned takes the index, finds it and accesses the 'messages' content. It goes through
    the messages and attaces it to returned_messages until k == 50 which it will then return the
    returned_messages variable.
    '''
    returned_messages = []

    message_store = store['channels'][channel_index]['messages']

    if message_store == []:
        return returned_messages

    for message_index in range(start, end):
        returned_messages.append(message_store[message_index])

    return returned_messages


def return_member_information(u_id, store):
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return {
                'u_id': user['auth_user_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle']
            }
