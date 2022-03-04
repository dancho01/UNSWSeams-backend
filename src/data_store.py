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
    'channels': []
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


# data = {
#     "users": [
#         {
#             "id": 1,
#             "name": "user1",
#             "global_permissions": 1,
#         },
#         {
#             "id": 2,
#             "name": "user2",
#             "global_permissions": 2,
#         },
#     ],
#     "channels": [
#         {
#             "id": 1,
#             "name": "channel1",
#             "all_members": [2, 4, 6, 8, 10], #authorized member ids (if its private)
#             "owner_members" : [1, 2, 3]  #user_id for admins
#             "is_public": False,
#             "messages": [
#                 {
#                     "message_id": 1,
#                     "u_id": 1,
#                     "message": "Hello world",
#                     "time_created": 4132,
#                 },
#                 {
#                     "message_id": 1,
#                     "u_id": 1,
#                     "message": "Hello world",
#                     "time_created": 2313,
#                 },
#             ],
#         },
#     ],
# }


# checkValidChannel checks all the channels within the data structure, if it finds a matching channel.
# If it finds a match, it will return 1 and the index number after it, else return 0.


def checkValidChannel(channel_id, data_store):

    channel_id = data_store['channels']

    for i in range(len(channel_id)):
        if channel_id[i]['name'] == channel_id:
            return 1, i

    return 0

# checkAuthorization loops through the authorized users within a channel, returning a 1 if this user is authorized
# and a 0 if they are not.


def checkAuthorization(auth_user_id, index, data_store):

    channel_authorization = data_store['channels'][index]['all_members']
    if auth_user_id in channel_authorization:
        return 1
    else:
        return 0

# messagesReturned takes the channelIndex, finds it and accesses the 'messages' content. It goes through
# the messages and attaces it to returnedMessages until k == 50 which it will then return the
# returnedMessages variable.


def messagesReturned(channelIndex, start, data_store):

    returnedMessages = []

    subject = data_store['channels'][channelIndex]

    k = 0

    for i in subject['messages']:
        if k == 50:
            return returnedMessages
        returnedMessages.append(i)
        k += 1


def create_member_dictionary(id_list, store):

    member_dict = []

    for id in id_list:
        member_dict.append(return_member(id, store))

    return member_dict


def return_member(id, store):
    for user_index in range(len(store['users'])):
        if store['users'][user_index]['id'] == id:
            return store['users'][user_index]
