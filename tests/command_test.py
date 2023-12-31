import pytest
import requests
import json
import time
from src import config
from src.data_store import data_store


@pytest.fixture
def create_first_user():
    '''
        Fixture for creating first user
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1 = user1.json()
    return user1


@pytest.fixture
def create_second_user():
    '''
        Fixture for creating second user
    '''
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                                                 'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2 = user2.json()
    return user2


@pytest.fixture
def create_third_user():
    '''
        Fixture for creating second user
    '''
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'tessstemail@gmail.com',
                                                                 'password': 'hello!!!!', 'name_first': 'Daniel', 'name_last': 'Chode'})
    user3 = user3.json()
    return user3


@pytest.fixture
def create_public_channel(create_first_user, create_second_user, create_third_user):
    '''
        Creates a public channel with 2 users, user2 is admin
    '''
    user1, user2, user3 = create_first_user, create_second_user, create_third_user

    ch1 = requests.post(config.url + 'channels/create/v2',
                        json={'token': user2['token'], 'name': 'ch1', 'is_public': True})

    channel1_data = ch1.json()

    requests.post(config.url + 'channel/addowner/v1', json={'token': user2['token'], 'channel_id': channel1_data['channel_id'],
                                                            'u_id': user2['auth_user_id']})

    requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'], 'channel_id': channel1_data['channel_id']})

    requests.post(config.url + 'channel/join/v2', json={
        'token': user3['token'], 'channel_id': channel1_data['channel_id']})

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'ch1': channel1_data,
    }


@pytest.fixture
def create_public_channel_no_owner(create_first_user, create_second_user, create_third_user):
    '''
        Creates a public channel, no owner
    '''
    user1, user2, user3 = create_first_user, create_second_user, create_third_user

    ch1 = requests.post(config.url + 'channels/create/v2',
                        json={'token': user2['token'], 'name': 'ch1', 'is_public': True})

    channel1_data = ch1.json()

    requests.post(config.url + 'channel/addowner/v1', json={'token': user2['token'], 'channel_id': channel1_data['channel_id'],
                                                            'u_id': user2['auth_user_id']})

    requests.post(config.url + 'channel/join/v2', json={
        'token': user1['token'], 'channel_id': channel1_data['channel_id']})

    requests.post(config.url + 'channel/leave/v1', json={
        'token': user2['token'], 'channel_id': channel1_data['channel_id']})

    requests.post(config.url + 'channel/join/v2', json={
        'token': user2['token'], 'channel_id': channel1_data['channel_id']})

    requests.post(config.url + 'channel/join/v2', json={
        'token': user3['token'], 'channel_id': channel1_data['channel_id']})

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'ch1': channel1_data,
    }


'''
    Invalid command
'''


def test_invalid_command(create_public_channel):
    '''
        Tests for a command that does not exist
    '''
    command = "/invalidcommand"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 400


'''
    /help
'''


def test_help(create_public_channel):
    '''
        Tests the /help function
    '''
    command = "/help"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


'''
    /dbot and /abot
'''


def test_deactivate_bot(create_public_channel):
    '''
        Testing to see if deactivating bot works
    '''
    command = "/dbot"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


def test_deactivate_bot_no_perms(create_public_channel):
    '''
        Testing to see if deactivating bot will raise an error when the user
        does not have the right permissions
    '''
    command = "/dbot"
    ch1, user3 = create_public_channel['ch1'], create_public_channel['user3']
    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 403


def test_activate_bot(create_public_channel):
    '''
        Testing to see if activating bot works
    '''
    command = "/abot"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


def test_activate_bot_no_perms(create_public_channel):
    '''
        Testing to see if activating bot will raise an error when the user
        does not have the right permissions
    '''
    command = "/abot"
    ch1, user3 = create_public_channel['ch1'], create_public_channel['user3']
    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 403


def test_activate_bot_no_owner(create_public_channel_no_owner):
    '''
        Testing to see if /abot will work when there are no owner members in the channel
    '''
    command = "/abot"
    ch1, user3 = create_public_channel_no_owner['ch1'], create_public_channel_no_owner['user3']
    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


def test_deactivate_bot_no_owner(create_public_channel_no_owner):
    '''
        Testing to see if /dbot will work when there are no owner members in the channel
    '''
    command = "/dbot"
    ch1, user3 = create_public_channel_no_owner['ch1'], create_public_channel_no_owner['user3']
    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


def test_command_deactivated_bot(create_public_channel):
    '''
        Testing to see if any commands will work if there is no bot active
    '''
    command = "/dbot"
    command1 = "/clearchat"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command1})

    assert response.status_code == 400


'''
    /timeout
'''


def test_time_out(create_public_channel):
    '''
        Testing timeout is successful
    '''
    command = "/timeout firstlast 1"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})
    time.sleep(2)
    assert response.status_code == 200


def test_time_invalid_params(create_public_channel):
    '''
        /timeout does not have the required params inputted
    '''
    command = "/timeout firstlast"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 400


def test_time_out_message_no_perms(create_public_channel):
    '''
        Tests if user who calls /timeout has no perms
    '''
    command = "/timeout firstlast 2"
    ch1, user3 = create_public_channel['ch1'], create_public_channel['user3']
    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 403


def test_time_out_message(create_public_channel):
    '''
        Tests to see if an error is raised after a user is timed out and they try
        to send a message
    '''
    command = "/timeout firstlast 2"
    ch1, user1, user2 = create_public_channel['ch1'], create_public_channel['user1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': "Hello"})

    assert response.status_code == 403


'''
    /clearchat
'''


def test_clear_chat(create_public_channel):
    '''
        Testing if clearing chat is successful with sufficient perms
    '''
    command = "/clearchat"
    ch1, user1, user2 = create_public_channel['ch1'], create_public_channel['user1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': "hey!"})
    requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': ch1['channel_id'], 'message': "Hello"})
    m1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user2['token'], 'channel_id': ch1['channel_id'], 'start': 0})

    message_response = m1.json()

    assert len(message_response['messages']) == 2

    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    m1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user2['token'], 'channel_id': ch1['channel_id'], 'start': 0})

    message_response = m1.json()

    assert len(message_response['messages']) == 0

    assert response.status_code == 200


def test_clear_chat_no_perms(create_public_channel):
    '''
        Testing if an error is raised if chat is cleared when the user has no perms
    '''
    command = "/clearchat"
    ch1, user3 = create_public_channel['ch1'], create_public_channel['user3']

    response = requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 403


'''
    /reset
'''


def test_reset(create_public_channel):
    '''
        Tests if /reset works if user is a global owner
    '''
    command = "/reset"
    ch1, user1 = create_public_channel['ch1'], create_public_channel['user1']
    lr = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                             'channel_id': ch1['channel_id'], 'message': command})
    assert lr.status_code == 200

    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'testemail@gmail.com',
                                                                       'password': 'elephant130'})

    assert login_response.status_code == 400


def test_reset_not_global_owner(create_public_channel):
    '''
        Tests to see if an error is raised when /reset is called when user is not a
        global owner
    '''
    command = "/reset"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    lr = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                             'channel_id': ch1['channel_id'], 'message': command})

    assert lr.status_code == 403


'''
    /startpoll
'''


def test_start_poll(create_public_channel):
    '''
        Tests to see if a poll is started successfully
    '''
    command = "/startpoll food chinese japanese"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 200


def test_start_poll_already_exists(create_public_channel):
    '''
        Tests to see if an error is raised when a poll is started when a poll
        already exists
    '''
    command = "/startpoll food chinese japanese"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 400


def test_start_invalid_params(create_public_channel):
    '''
        Tests to see if an error is raised when not enough params are entered
    '''
    command = "/startpoll 2 3 "
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 400


'''
    /addpolloption
'''


def test_addpolloption(create_public_channel):
    '''
        Tests to see if /addpolloption works as intended
    '''
    command = "/startpoll 2 3 4"
    command1 = "/addpolloption 1 2 3"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command1})
    assert response.status_code == 200


def test_no_poll_addpolloption(create_public_channel):
    '''
        Tests if an error is raised when options are added when no poll exists
    '''
    command = "/addpolloption 1 2 3"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})

    assert response.status_code == 400


'''
    /vote
'''


def test_vote(create_public_channel):
    '''
        Tests if vote works as intended
    '''
    command = "/startpoll 2 3 4"
    command1 = "/vote 2"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command1})
    assert response.status_code == 200


def test_change_vote(create_public_channel):
    '''
        Tests if calling /vote after you have already voted works
    '''
    command = "/startpoll 2 3 4"
    command1 = "/vote 3"
    command2 = "/vote 4"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command1})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command2})
    assert response.status_code == 200


def test_vote_no_poll(create_public_channel):
    '''
        Testing if voting when there is no poll raises an error
    '''
    command = "/vote 2"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']

    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})
    assert response.status_code == 400


'''
    /endpoll
'''


def test_endpoll(create_public_channel):
    '''
        Tests if endpoll works as intended
    '''
    command = "/startpoll 2 3 4"
    command1 = "/endpoll"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command1})
    assert response.status_code == 200


def test_voted_endpoll_one_winner(create_public_channel):
    '''
        Tests where there is one most popular
    '''
    command = "/startpoll 2 3 4"
    command2 = "/vote 4"
    command4 = "/endpoll"
    ch1, user2, user3 = create_public_channel['ch1'], create_public_channel['user2'], create_public_channel['user3']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command2})
    requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command2})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command4})
    assert response.status_code == 200


def test_voted_endpoll_multiple_votes(create_public_channel):
    '''
        Tests multiple people voting, second option is more popular than the first
    '''
    command = "/startpoll 2 3 4"
    command1 = "/vote 3"
    command2 = "/vote 4"
    command4 = "/endpoll"
    ch1, user1, user2, user3 = create_public_channel['ch1'], create_public_channel[
        'user1'], create_public_channel['user2'], create_public_channel['user3']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command1})
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command2})
    requests.post(config.url + 'message/send/v1', json={'token': user3['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command2})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command4})
    assert response.status_code == 200


def test_winner_endpoll(create_public_channel):
    '''
        Tests if the most popular option works as intended
    '''
    command = "/startpoll 2 3 4"
    command1 = "/vote 2"
    command2 = "/endpoll"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command1})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command2})
    assert response.status_code == 200


def test_endpoll_no_poll(create_public_channel):
    '''
        Tests if an error is raised if there is no poll when /endpoll is called
    '''
    command = "/endpoll"
    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})
    assert response.status_code == 400


def test_endpoll_diff_user(create_public_channel):
    '''
        Test if an error is raised when a user different to the one who started
        the poll tries to end it
    '''
    command = "/startpoll 2 3 4"
    command1 = "/endpoll"
    ch1, user1, user2 = create_public_channel['ch1'], create_public_channel['user1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command1})
    assert response.status_code == 403


'''
    language filter
'''


def test_language_filter_off(create_public_channel):
    '''
        Tests that no error is raised when swearing if the bot is off
    '''
    message = "shit"
    command = "/dbot"

    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': command})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': message})

    assert response.status_code == 200


def test_language_filter_on(create_public_channel):
    '''
        Tests if the filter works when the bot is on
    '''
    message = "shit"

    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': message})

    assert response.status_code == 200


def test_language_filter_timedout(create_public_channel):
    '''
        Tests that if a user is timed out after swearing 3 times
    '''
    message = "shit"

    ch1, user2 = create_public_channel['ch1'], create_public_channel['user2']
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': message})
    requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': ch1['channel_id'], 'message': message})
    response = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                                   'channel_id': ch1['channel_id'], 'message': message})

    assert response.status_code == 200
