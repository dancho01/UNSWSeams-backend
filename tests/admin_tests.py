import pytest
import requests
import json
from src import config
from src.global_helper import check_valid_user

def test_admin_user_remove_u_id_not_valid():
    """
    u_id does not refer to a valid user
    """
