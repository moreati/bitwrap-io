"""
test calls against the json-rpc API

"""
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
import bitwrap_pnml
from bitwrap_pnml.test import ApiTest
import ujson as json


class SchemaTest(ApiTest):
    """
    setup rpc endpoint and invoke ping method
    """

    @inlineCallbacks
    def test_view(self):
        """ retrieve schema xml """
        # FIXME actually test state
        res = yield ApiTest.fetch('pnml/metaschema.xml')
        assert res.code == 200

