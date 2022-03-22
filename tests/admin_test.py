import pytest
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1, channel_details_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1

"""
    tests for admin/userpermission/change/v1
"""
