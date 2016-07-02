import pytest

import bitwrap_io
import urllib
from bitwrap_io.api import app as _app
import json

bitwrap_io.start()

@pytest.fixture
def client(request):

    def teardown():
        print("teardown")

    request.addfinalizer(teardown)

    return _app.test_client()

@pytest.fixture
def schema():
    return 'karmanom.com'

@pytest.fixture
def api_message():
     return {
         'signal': { 'schema': 'karmanom.com', 'action': 'positive_tip' },
         'addresses': { 'sender': 'zim', 'target': 'dib' }
     }

@pytest.fixture
def api_response():
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

def test_api_transform(client, schema, api_message, api_response):
    r = client.get('/api', query_string={ 'msg': json.dumps(api_message) } )
    res = json.loads(r.data)

    assert 202 == r.status_code
    #assert api_response == res # FIXME

