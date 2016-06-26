import pytest
import bitwrap_io

@pytest.fixture
def app():
    pass

@pytest.fixture
def schema():
    return 'karmanom.com'

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

def test_api_transform(schema, response):
    assert True
