import pytest
import bitwrap_io
import os

@pytest.fixture
def karmanom():
    return bitwrap_io.get('karmanom.com')

@pytest.fixture
def response():
    return {
        'cache': {
            'control': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'dib': [0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 1],
            'zim': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
         },
        'context': {
            'action': [0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, -1],
            'control': [ 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            'target': [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0 ],
            'sender': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1 ],
         },
         'errors': [],
         'message': {
            'addresses': {'sender': 'zim', 'target': 'dib'},
            'signal': {'action': 'positive_tip', 'role': 1, 'schema': 'karmanom.com'}
         }
     }


def test_console(karmanom, response):
    req = karmanom.console().sender('zim').target('dib').send('positive_tip').session
    res = karmanom.machine.execute(karmanom.machine.new_request(req))
    assert response == res
