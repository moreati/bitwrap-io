import bitwrap
import pytest
import os


@pytest.fixture
def karmanom():
    _dir = os.path.dirname(__file__)
    json_schema = os.path.join(_dir, 'machine/karmanom.com.json')
    return bitwrap.open_json('karmanom.com', json_schema)


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
            'signal': {'action': 'positive_tip', 'role': 1}
         }
     }


def test_machine(karmanom, response):
    r = karmanom.console().sender('zim').target('dib').send('positive_tip').commit()
    assert response == r
