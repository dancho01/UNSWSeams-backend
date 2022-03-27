from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import check_valid_token
from src.global_helper import check_valid_user, check_global_owner
from src.admin_helper import remove_user_name, remove_user_messages, remove_user_from_channels, only_global_owner_check, remove_from_session_list, check_and_set_new_permissions


def admin_user_remove_v1(token, u_id):
    '''
    Given a user by their u_id, remove them from the Seams. This means they should be removed from all 
    channels/DMs, and will not be included in the list of users returned by users/all. 
    Seams owners can remove other Seams owners (including the original first owner). 
    Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
    Their profile must still be retrievable with user/profile, however name_first should be 'Removed' 
    and name_last should be 'user'. The user's email and handle should be reusable.

    Arguments:
        token           string      - token of the user that is inviting
        u_id            int         - id of the user that is being invited

    Exceptions:
        AccessError     - Occurs when the authorised user is not a global owner
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is the only global owner

    Return Value:
        Returns empty dict as required by spec
    '''
    auth_user_id = check_valid_token(token)['u_id']

    if check_global_owner(auth_user_id) == False:
        raise AccessError("authorised user is not a global owner")

    check_valid_user(u_id)

    only_global_owner_check(u_id)

    remove_user_name(u_id)              # Turns their name to 'Removed user' in user database
    
    remove_user_from_channels(u_id)     # Removes users from all channels and dms

    remove_user_messages(u_id)          # Edits their messages to 'Removed user' in all dms and channels

    remove_from_session_list(u_id)      # Removes the user from the session_list
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Function: Given a user by their user ID, set their permissions to new permissions described by permission_id.
    Parameters:{ token, u_id, permission_id }
    Return Type:{}
    """
    auth_user_id = check_valid_token(token)['u_id']
    if check_global_owner(auth_user_id) == False:
        raise AccessError('authorised user is not a global owner')
    check_valid_user(u_id)

    if permission_id != 1 and permission_id != 2:
        raise InputError('permission_id is invalid')

    only_global_owner_check(u_id)

    check_and_set_new_permissions(u_id, permission_id)

    return {}
