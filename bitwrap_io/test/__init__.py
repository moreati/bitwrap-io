"""
run tests against a webserver running in the same reactor

NOTE: this test uses port 8888 on localhost
"""

from twisted.application import internet
from twisted.trial.unittest import TestCase
import cyclone.httpclient
from bitwrap_io.storage import Storage
from bitwrap_io.api import factory as ApiFactory

IFACE = '127.0.0.1'
PORT = 8888

class ApiTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        """ recreate database and start tcp endpoint """
        Storage.truncate()
        self.service = internet.TCPServer(PORT, ApiFactory(), interface=IFACE)
        self.service.startService()

    def tearDown(self):
        """ stop tcp endpoint """
        self.service.stopService()
        
    @staticmethod
    def url(resource):
        """ bulid a url for test endpoint """
        return 'http://%s:%s/%s' % (IFACE, PORT, resource)

    @staticmethod
    def client(resource):
        """ rpc client """
        return cyclone.httpclient.JsonRPC(ApiTest.url(resource))

    @staticmethod
    def fetch(resource, **kwargs):
        """ async request with httpclient"""
        return cyclone.httpclient.fetch(ApiTest.url(resource), **kwargs)
