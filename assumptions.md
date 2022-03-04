# Assumptions

## auth.py

### Test assumptions for iteration 1

#### auth_login_v1

#### auth_register_v1

---

## channel.py

### Test assumptions for iteration 1

#### channel_invite_v1

#### channel_details_v1

#### channel_messages_v1

    1. There is currently no function that will input messages to the channel, so in order to test the current functionalities we have access to, the tests will only consist of:
        1. InputError checking
        2. AccessError checking
        3. Invalid store value (store < 1)

#### channel_join_v1

---

## channels.py

### Test assumptions for iteration 1

#### channels_list_v1

#### channels_listall_v1

#### channels_create_v1

---

## other.py

### Test assumptions for iteration 1

#### clear_v1
