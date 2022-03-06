import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.error import InputError, AccessError
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
def create_second_public_channel_for_first_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    second_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name 2', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'second_new_channel_id': second_new_channel_id}

@pytest.fixture
def create_second_private_channel_for_first_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    second_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name 2', False)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'second_new_channel_id': second_new_channel_id}


@pytest.fixture
def create_second_user():
    auth_user2_id = auth_register_v1('another_email@domain.com',
                                     'Password2', 'First', 'Last')['auth_user_id']
    return {'auth_user2_id': auth_user2_id}

@pytest.fixture
def create_first_channel_for_second_user(create_second_user):
    auth_user2_id = create_second_user['auth_user2_id']
    third_new_channel_id = channels_create_v1(
        auth_user2_id, 'Channel Name 3', True)['channel_id']
    return {'auth_user2_id': auth_user2_id, 'third_new_channel_id' : third_new_channel_id}

# Test for channels_list_v1


# Testing if all public channels in server linked to the individual
def test_0_one_user_multiple_public_channels(create_first_channel_and_user, create_second_public_channel_for_first_user):  
    '''
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. Then the fixture 
        create_second_public_channel_for_first_user will produce a secod public channel for the first user. The assert is used to
        ensure that the user is able to recieve a non-empty dictionary from channels_list_v1.
    '''                                                    
    first_user_first_channel = create_first_channel_and_user 
    create_second_public_channel_for_first_user
    assert(channels_list_v1(first_user_first_channel['auth_user1_id']) != {})  


# Testing if all channels, public and private, linked to the individual
def test_1_one_user_multiple_mixed_channels(create_first_channel_and_user, create_second_private_channel_for_first_user):
    '''
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. Then the fixture 
        create_second_private_channel_for_first_user will produce a private channel for the first user. The assert is used to
        ensure that the user is able to recieve a non-empty dictionary from channels_list_v1.
    '''       
    first_user_first_channel = create_first_channel_and_user 
    create_second_private_channel_for_first_user
    assert(channels_list_v1(first_user_first_channel['auth_user1_id']) != {})  


# Testing if channels linked to specified users are listed
def test_2_multiple_users_multiple_channels(create_first_channel_and_user, create_first_channel_for_second_user):  
    '''
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. Fixture create_first_channel_for_second_user
        is used to create the second user and a channel they have created. The assert is used to ensure both users
        are able to recieve a non-empty dictionary from channels_list_v1.
    '''                                                             
    first_user_first_channel = create_first_channel_and_user
    second_user_first_channel = create_first_channel_for_second_user
    assert(channels_list_v1(first_user_first_channel['auth_user1_id']) != {}) 
    assert(channels_list_v1(second_user_first_channel['auth_user2_id']) != {}) 


# Testing if channels linked to specified users are listed
def test_3_user_no_channel(create_first_channel_and_user, create_second_user):   
    '''
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. Fixture create_second_user. The assert 
        is used to ensure that the second user revieves an empty dictionary from channels_list_v1, as they are not in any channels.
    '''                                                     
    create_first_channel_and_user
    second_user = create_second_user
    assert(channels_list_v1(second_user['auth_user2_id']) == {'channels': []}) 


# Testing if invalid user raises an AccessError
def test_4_invalid_user(create_first_channel_and_user):  
    '''
    Error raised:
        InputError: Checking if auth_user_id passed in is invalid.
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. The assert is used to ensure that 
        an invalid user requesting channels_list_v1 raises a AccessError. 
    '''                                         
    first_user_first_channel = create_first_channel_and_user
    with pytest.raises(AccessError):
       channels_list_v1(first_user_first_channel['auth_user1_id'] + 1)


# Test for channels_listall_v1

# Testing output type as the testing requires going into the data    
def test_0_output_type(create_first_channel_and_user, create_second_public_channel_for_first_user): 
    '''
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. Then the fixture 
        create_second_public_channel_for_first_user will produce a second public channel for the first user. The assert is used to
        ensure that the user is able to recieve a non-empty dictionary from channels_listall_v1.
    '''             
    first_user_first_channel = create_first_channel_and_user
    create_second_public_channel_for_first_user                                                                                     
    assert(channels_listall_v1(first_user_first_channel['auth_user1_id']) != {})


# Testing if invalid user raises an AccessError
def test_1_invalid_user(create_first_channel_and_user):     
    '''
    Error raised:
        InputError: Checking if auth_user_id passed in is invalid.
    Explanation:
        Fixture create_first_channel_and_user is used to create the first user and channel. The assert is used to ensure that 
        an invalid user requetsing channels_listall_v1 raises a AccessError. 
    '''                                                                                    
    first_user_first_channel = create_first_channel_and_user  
    create_second_public_channel_for_first_user                                                                                     
    with pytest.raises(AccessError):
       channels_listall_v1(first_user_first_channel['auth_user1_id'] + 1)



# channels_create_v1 tests
# Tests for invalid name for public channel
def test_invalid_channel_name_public(create_first_user): 
    '''
    Error raised:
        InputError
    Explanation:
        When the length of the name entered in for a public channel is less
        than 1 or more than 20 characters     
    '''  
    first_u_id = create_first_user['auth_user1_id']
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, '', True)
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, 'abcdefghijklmnopqrstuvwxyz', True)

# Tests for invalid name for private channel
def test_invalid_channel_name_private(create_first_user):
    '''
    Error raised:
        InputError
    Explanation: 
        When the length of the name entered in for a private channel is less
        than 1 or more than 20 characters  
    '''
  
    first_u_id = create_first_user['auth_user1_id']
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, '', False)
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, 'abcdefghijklmnopqrstuvwxyz', False)

# Tests for invalid user_id and invalid channel name 
def test_invalid_name_and_user_id():
    '''
    Errors raised:
        AccessError 
    Explanation: 
        When an invalid user id and invalid channel name is passed in 
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, '', True)
    with pytest.raises(AccessError):
        channels_create_v1(1, 'abcdefghijklmnopqrstuvwxyz', True)

# Test for no user registered
def test_no_user_registered():
    '''
    Errors raised:
        AccessError
    Explanation:
        When an invalid user id is passed in, as there are no users registered   
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, 'channelname', True)
        
# Test for invalid user id passed in 
def test_invalid_user_id(create_first_user):
    '''
    Error raised:
        AccessError
    Explanation:
        When user id passed in does not yet exist  
    '''
    first_u_id = create_first_user['auth_user1_id']
    with pytest.raises(AccessError):
        channels_create_v1(first_u_id + 1, 'validname', True)

# Test for correct return type
def test_correct_return_type(create_first_channel_and_user):
    '''
    Explanation: 
        Makes sure that the correct return type is returned   
    '''
    channel_return = create_first_channel_and_user
    channel_id = channel_return['first_new_channel_id']
    assert type(channel_id) is int
    
