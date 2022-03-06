# Assumptions

## auth.py

### Test assumptions for iteration 1

#### auth_login_v1

#### auth_register_v1

---

## channel.py

### Test assumptions for iteration 1

#### channel_invite_v1

1. Assumes there is at least 1 user in Seams for a channel to be created to invite others. If no user at all, will throw an access error.

#### channel_details_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing. Only checking return type. 


#### channel_messages_v1

#### channel_join_v1

---

## channels.py

### Test assumptions for iteration 1

#### channels_list_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing.

#### channels_listall_v1

1. Cannot check return value without knowing the data structure and making it white box testing. Therefore, we cannot test the return value is correct other than if the return type is correct with black box testing.

#### channels_create_v1

---

## other.py

### Test assumptions for iteration 1

#### clear_v1
