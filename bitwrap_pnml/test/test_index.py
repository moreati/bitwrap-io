"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest
import ujson as json


class IndexTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """
        
    @inlineCallbacks
    def test_api_version(self):
        """ retrieve api version from index """
        res = yield ApiTest.fetch('version')
        info = json.loads(res.body)
        assert info['bitwrap_pnml.api'] == 'v2'
