import pytest
from src.other import clear_v1



def test_clear_v1():
    data = {
        'users': [
            {
                'id': 1,
                'name' : 'user1',
            },
            {
                'id': 2,
                'name' : 'user2',
            },
        ],
        'channels': [
            {
                'id': 1,
                'name' : 'channel1',
                'authorized' : [2, 4, 6, 8, 10],
            },
            {
                'id': 2,
                'name' : 'channel2',
                'authorized' : [1, 3, 5, 7, 9],
            },
            
        ]
    }

    assert(clear_v1() == {})
    