# Assumptions

## Channel.py
### Test assumptions for iteration 1
#### channel_messages_v1
##### Input Error
- assuming auth_id = 5 : valid, user_id = 6 : valid, start >= 0 : valid
- For tests related to invalid channel_id, the tests are currently not usable as data_store.py is not yet populated.

###### Test_0
- assumes auth_id: valid, user_id: valid, start: invalid
###### Test_1
- assumes auth_id: invalid, user_id: valid, start: invalid
###### Test_2
- assumes auth_id: valid, user_id: invalid, start: invalid
###### Test_3
- assumes auth_id: invalid, user_id: invalid, start: invalid
###### Test_4
- assumes auth_id: invalid, user_id: valid, start: valid
###### Test_5
- assumes auth_id: invalid, user_id: invalid, start: valid
###### Test_6
- assumes auth_id: valid, user_id: invalid, start: valid

##### Access Error
- For tests related to access error, the tests are currently not usable as data_store.py is not yet populated.

## Other.py
### Test assumptions for iteration 1
#### clear_v1
- Assumes the data structure will be similar to the one that has been provided in the test function, however the provided function is only a preliminary version which could be subject to change in future iterations.