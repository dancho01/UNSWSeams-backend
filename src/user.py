from src.token import check_valid_token
from src.global_helper import check_valid_user
from src.users_helpers import return_profile
from src.user_helper import return_notifications
from src.data_store import data_store
from src.users_helpers import return_users_information


def user_profile_v1(token, u_id):
    '''
        Returns a given user's profile 
    '''

    check_valid_token(token)

    check_valid_user(u_id)

    profile_info = return_profile(u_id)

    return {'user': profile_info}

def user_stats_v1(token):
'''
    Outputs: Dictionary of shape {
 channels_joined: [{num_channels_joined, time_stamp}],
 dms_joined: [{num_dms_joined, time_stamp}],
 messages_sent: [{num_messages_sent, time_stamp}],
 involvement_rate
}
'''
    store = data_store.get()

    auth_user_id = check_valid_token(token)['u_id']
    involvement_rate = 0.0

    for user in store['users']:
        if user['auth_user_id'] == auth_user_id
            involvement_rate = sum(user['stats']["total_channels_joined"], user['stats']["total_dms_joined"], user['stats']["total_messages_sent"]) / 
                sum(store['stats']['workspace_stats']['total_num_channels'], store['stats']['workspace_stats']['total_num_dms'], 
                store['stats']['workspace_stats']['total_num_messages'])
            user['stats']['user_stats']['involvement_rate'] = involvement_rate
            return {'user_stats': user['stats']['user_stats']}

def users_stats_v1(token):
'''
    returns Dictionary of shape {
     channels_exist: [{num_channels_exist, time_stamp}], 
     dms_exist: [{num_dms_exist, time_stamp}], 
     messages_exist: [{num_messages_exist, time_stamp}], 
     utilization_rate 
    }

'''
    store = data_store.get()
    auth_user_id = check_valid_token(token)['u_id']
    utilization_rate = 0.0  # = num_users_who_have_joined_at_least_one_channel_or_dm / num_users

    num_users_who_have_joined_at_least_one_channel_or_dm = 0
    num_users = len(return_users_information())
    for user in store['users']:
        if user['stats']["total_channels_joined"] > 0 or user['stats']["total_dms_joined"] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1

    utilization_rate = num_users_who_have_joined_at_least_one_channel_or_dm / num_users
    store['workspace_stats']['utilization_rate'] = utilization_rate

    return {'workspace_stats': store['stats']['workspace_stats']}


def notifications_get_v1(token):
    user_id = check_valid_token(token)['u_id']

    user_notifications = return_notifications(user_id)
    print(user_notifications)
    return {'notifications': user_notifications}

