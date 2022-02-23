from error import InputError, AccessError
global data

data = {
    'users': [
        {
            'id': 1,
            'name' : 'user1',
        },
        {
            'id': 2,
            'name' : 'user2',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'authorized' : [2, 4, 6, 8, 10],
            'messages' : [
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
            ]
        },
        {
            'id': 2,
            'name' : 'channel2',
            'authorized' : [1, 3, 5, 7, 9],
        },
        
    ]
}

# checkValidChannel checks all the channels within the data structure, if it finds a matching channel.
# If it finds a match, it will return 1 and the index number after it, else return 0.

def checkValidChannel(channel_id):
    
    channelId = data['channels']
    
    for i in range(len(channelId)):
        if channelId[i]['id'] == channel_id:
            print(channelId[i])
            print(i)
            return 1, i
        
    return 0

# checkAuthorization loops through the authorized users within a channel, returning a 1 if this user is authorized
# and a 0 if they are not.

def checkAuthorization(auth_user_id, index):
    
    channelAuthorization = data['channels'][index]['authorized']
    print(channelAuthorization)
    if auth_user_id in channelAuthorization:
        return 1
    else:
        return 0
    
# messagesReturned takes the channelIndex, finds it and accesses the 'messages' content. It goes through
# the messages and attaces it to returnedMessages until k == 50 which it will then return the
# returnedMessages variable.

def messagesReturned(channelIndex, start):
    
    returnedMessages = []
    
    subject = data['channels'][channelIndex]
    
    k = 0
    
    for i in subject['messages']:
        if k == 50:
            return returnedMessages
        returnedMessages.append(i)
        k += 1