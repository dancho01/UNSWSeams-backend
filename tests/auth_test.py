import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError
from src.other import clear_v1

'''
Pytest fixtures
'''


@pytest.fixture
def create_first_user():
    clear_v1()
    auth_user1_id = auth_register_v1(
        'valid_email@domain.com', 'Password1', 'First', 'Last')['auth_user_id']
    return {'auth_user1_id': auth_user1_id}


@pytest.fixture
def create_first_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'first_new_channel_id': first_new_channel_id}


@pytest.fixture
def create_second_user():
    auth_user2_id = auth_register_v1('another_email@domain.com',
                                     'Password2', 'First', 'Last')['auth_user_id']
    return {'auth_user2_id': auth_user2_id}


auth_register_v1('awinstonchurchhill@gmail.com',
                 'winniepooh', 'winstoney', 'churchhillon')
>>>>>>> 070854df7220ecf088d1d1cc13e6739fc78866f2


def test_rego_invalid_fname():
    clear_v1()
    # with pytest.raises(InputError):
    #     auth_register_v1('winstonchurchhill@gmail.com',
    #                      'winniepooh', 'w!nston', 'churchhill')
    # with pytest.raises(InputError):
    #     auth_register_v1('winstonchurchhill@gmail.com',
    #                      'winniepooh', 'winst0n', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', '', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh',
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'churchhill')


def test_rego_invalid_lname():
    clear_v1()
    # with pytest.raises(InputError):
    #     auth_register_v1('winstonchurchhill@gmail.com',
    #                      'winniepooh', 'winston', 'churchh!ll')
    # with pytest.raises(InputError):
    #     auth_register_v1('winstonchurchhill@gmail.com',
    #                      'winniepooh', 'winston', 'churchh1ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', 'winston', '')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston',
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')


def test_rego_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail@com',
                         'winniepooh', 'winston', 'churchhill')


def test_rego_invalid_pass():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         '', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'pooh', 'winston', 'churchh!ll')


def test_rego_no_repeats():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', 'winston', 'churchhill')


def test_handle_partial():
    clear_v1()
    auth_register_v1('awinstonchurchhill@gmail.com',
                     'winniepooh', 'winstoney', 'churchhillon')
    auth_register_v1('bwinstonchurchhill@gmail.com',
                     'winniepooh', 'winst0tney', 'churchhillon')
    auth_register_v1('cwinstonchurchhill@gmail.com',
                     'winniepooh', 'winstoney', 'churchhillon') == 1


def test_login_invalid_email():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('wchurchhill@gmail.com', 'winniepooh')


def test_login_invalid_pass():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmail.com', 'poohwinnie')


def test_login_invalid_email_format1():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhillgmail.com', 'winniepooh')


def test_login_invalid_email_format2():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmailcom', 'winniepooh')


def test_rego_to_login():
    clear_v1()
    rego_id = auth_register_v1(
        'winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    login_id = auth_login_v1('winstonchurchhill@gmail.com', 'winniepooh')
    assert rego_id == login_id
