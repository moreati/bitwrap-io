"""
test calls against the json-rpc API

"""
import json
import cyclone.httpclient
from twisted.internet.defer import inlineCallbacks
from bitwrap_io.test import ApiTest
import bitwrap_io

bitwrap_io('octothorpe')


class EventTest(ApiTest):
    """
    """

    cli = ApiTest.client('api')

    @inlineCallbacks
    def test_transform(self):


        res = yield self.cli.transform({
            "schema": "octothorpe",
            "oid": "fakeoid-trial1",
            "action": "BEGIN"
        })

        #self.assertEqual(res['event']['state'], [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0])
        print json.dumps(res, indent=4)

        #res = yield self.cli.transform({
        #    "schema": "octothorpe",
        #    "oid": "fakeoid-trial1",
        #    "action": "X11"
        #})

        #self.assertEqual(res['event']['state'], [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0])
        #print json.dumps(res, indent=4)
