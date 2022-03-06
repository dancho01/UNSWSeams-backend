# Assumptions

### Test assumptions for iteration 1

## auth.py

#### auth_login_v1

#### auth_register_v1

1. Assumes that the first user that is registered is the ONLY one who has global owner permissions as there is currently no function to upgrade memberships.

---

## channel.py

#### channel_invite_v1

1. Assumes there is at least 1 user in Seams for a channel to be created to invite others. If no user at all, will throw an access error.

#### channel_details_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing.

#### channel_messages_v1

```
def test_channel_no_messages(create_first_channel_and_user):
    '''
    Return checked:
        Checking to see if details returns a dictionary structure

    Explanation:
        Passing in all valid parameters where since there are no messages, the returned
        'messages' key is expected to be an empty list.
    '''
    assert(channel_messages_v1(create_first_channel_and_user['auth_user1_id'],
           create_first_channel_and_user['first_new_channel_id'], -1)['messages'] == [])
```

1. We are assuming that the inputted start index will always be larger than 0, we initially thought
   about using this test but due to the start index checking and lack of function to input messages but
   realized that the index -1 is pointing to the end of the list so it is not possible. This test will be implemented in the next iteration to check the behavior of a channel with no messages.

#### channel_join_v1

1. Assumes the global owner can join both private and public channels that they are not apart of.

---

## channels.py

#### channels_list_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing.

#### channels_listall_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing.

#### channels_create_v1

---
