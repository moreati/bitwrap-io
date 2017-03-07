"""
run tests against a webserver running in the same reactor

NOTE: this test uses port 8888 on localhost
"""

import cyclone.httpclient
from twisted.application import internet
from twisted.trial.unittest import TestCase
from bitwrap_io.api import factory as ApiFactory
import bitwrap_io.storage

IFACE = '127.0.0.1'
PORT = 8888

class ApiTest(TestCase):
    """ setup rpc endpoint and invoke ping method """

    def setUp(self):
        """ recreate database and start tcp endpoint """
        #pylint: disable=no-member
        self.service = internet.TCPServer(PORT, ApiFactory(), interface=IFACE)
        #pylint: enable=no-member
        self.service.startService()

    def tearDown(self):
        """ stop tcp endpoint """
        self.service.stopService()

    @staticmethod
    def url(resource):
        """ bulid a url using test endpoint """
        return 'http://%s:%s/%s' % (IFACE, PORT, resource)

    @staticmethod
    def client(resource):
        """ rpc client """
        return cyclone.httpclient.JsonRPC(ApiTest.url(resource))

    @staticmethod
    def fetch(resource, **kwargs):
        """ async request with httpclient"""
        return cyclone.httpclient.fetch(ApiTest.url(resource), **kwargs)
