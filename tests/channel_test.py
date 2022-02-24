import pytest
from src.channel import channel_messages_v1
from src.error import InputError, AccessError

# Test for invalid start                        #assuming auth_id = 5 : valid, user_id = 6 : valid, start >= 0 : valid

def test_0_invalid_start():                       
    with pytest.raises(InputError):             #assuming auth_id: valid, user_id: valid, start: invalid
        channel_messages_v1(5, 6, -1)          
    
def test_1_invalid_start():                      
    with pytest.raises(InputError):             #assuming auth_id: invalid, user_id: valid, start: invalid
        channel_messages_v1(4, 6, -100)         

def test_2_invalid_start():                    
    with pytest.raises(InputError):             #assuming auth_id: valid, user_id: invalid, start: invalid
        channel_messages_v1(4, 5, -32)
        
def test_3_invalid_start():
    with pytest.raises(InputError):             #assuming auth_id: invalid, user_id: invalid, start: invalid
        channel_messages_v1(3, 2, 24)
        
def test_4_invalid_channel():                    
    with pytest.raises(InputError):             #assuming auth_id: invalid, user_id: valid, start: valid
        channel_messages_v1(4, 6, 3)
        
def test5_invalid_channel():
    with pytest.raises(InputError):             #assuming auth_id: invalid, user_id: invalid, start: valid
        channel_messages_v1(7, 23, 3)
        
def test_6_invalid_authorization():
    with pytest.raises(AccessError):             #assuming auth_id: valid, user_id: invalid, start: valid
        channel_messages_v1(5, 14, 3)
        


        