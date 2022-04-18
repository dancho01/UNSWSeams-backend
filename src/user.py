from src.token import check_valid_token
from src.global_helper import check_valid_user
from src.data_store import data_store
from src.users_helpers import return_users_information, return_profile
from src.user_helper import return_notifications, return_user_handle, imgDown, crop, check_dimensions, check_image_type, check_url_status, newphoto
import urllib.request
from PIL import Image


def user_profile_v1(token, u_id):
    '''
        Args:
            token (str)
            u_id (int)

        Returns:
            A dictionary containing a given user's profile 
    '''

    check_valid_token(token)

    check_valid_user(u_id)

    profile_info = return_profile(u_id)

    return {'user': profile_info}


def user_stats_v1(token):
    """returns a users stats

    Args:
        token (str)

    Returns:
        user_stats: a dictionary containing a dictionary of user stats
    """
    store = data_store.get()

    auth_user_id = check_valid_token(token)['u_id']
    involvement_rate = 0.0

    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            numerator = sum([user['stats']["total_channels_joined"], user['stats']
                            ["total_dms_joined"], user['stats']["total_messages_sent"]])
            denominator = sum([store['stats']['total_num_channels'], store['stats']
                              ['total_num_dms'], store['stats']['total_num_messages']])
            if denominator != 0:
                involvement_rate = numerator / denominator
            involvement_rate = min(1.0, involvement_rate)
            user['stats']['user_stats']['involvement_rate'] = involvement_rate
            return {'user_stats': user['stats']['user_stats']}


def users_stats_v1(token):
    """Returns stats for workspace

    Args:
        token (str)

    Returns:
        dict: dict containing workspace stats
    """
    store = data_store.get()
    check_valid_token(token)['u_id']
    # = num_users_who_have_joined_at_least_one_channel_or_dm / num_users
    utilization_rate = 0.0

    num_users_who_have_joined_at_least_one_channel_or_dm = 0
    num_users = len(return_users_information())
    for user in store['users']:
        if user['stats']["total_channels_joined"] > 0 or user['stats']["total_dms_joined"] > 0:
            num_users_who_have_joined_at_least_one_channel_or_dm += 1

    utilization_rate = num_users_who_have_joined_at_least_one_channel_or_dm / num_users

    return {'workspace_stats': {
        'channels_exist': store['stats']['workspace_stats']['channels_exist'],
        'dms_exist': store['stats']['workspace_stats']['dms_exist'],
        'messages_exist': store['stats']['workspace_stats']['messages_exist'],
        'utilization_rate': utilization_rate
    }
    }


def notifications_get_v1(token):
    """Grabs notifications attached to a users profile

    Args:
        token (str)

    Returns:
        dictionary: dictionary key of notifications with its str list user_notifications
    """
    user_id = check_valid_token(token)['u_id']

    user_notifications = return_notifications(user_id)
    return {'notifications': user_notifications}


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    """
        User uploads a JPEG with the correct crop dimensions, changing its default
        profile picture in all of the given user instances in the data structure.
        Photo is unable to be uploaded if provided URL does not work, the image is not
        a JPEG, or incorrect crop dimensions are given.
    Args:
        token (string)
        img_url (string)
        x_start (int)
        y_start (int)
        x_end (int)
        y_end (int)

    Returns:
        {}
    """

    user_info = check_valid_token(token)
    handle = return_user_handle(user_info['u_id'])

    check_url_status(img_url)

    imgDown(img_url, handle)

    check_dimensions(x_start, y_start, x_end, y_end, handle)

    check_image_type(handle)

    crop(x_start, y_start, x_end, y_end, handle)

    newphoto(handle)

    return {}
