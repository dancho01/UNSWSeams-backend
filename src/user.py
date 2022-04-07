from src.token import check_valid_token
from src.global_helper import check_valid_user
from src.users_helpers import return_profile


def user_profile_v1(token, u_id):
    '''
        Returns a given user's profile 
    '''

    check_valid_token(token)

    check_valid_user(u_id)

    profile_info = return_profile(u_id)

    return {'user': profile_info}

# def user_stats_v1(token):
# #     Outputs: Dictionary of shape {
# #  channels_joined: [{num_channels_joined, time_stamp}],
# #  dms_joined: [{num_dms_joined, time_stamp}],
# #  messages_sent: [{num_messages_sent, time_stamp}],
# #  involvement_rate
# # }

#     store = data_store.get()


#     return {'user_stats': stats_info}