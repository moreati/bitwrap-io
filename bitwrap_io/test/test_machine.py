""" bitwrap.test.test_machine """

from twisted.internet import defer
from bitwrap_io.test import ApiTest

class MachineTest(ApiTest):
    """ test api methods not dealing with events"""

    cli = ApiTest.client('api')

    def test_machine_api(self):
        """ test a sequence of tic-tac-toe transformations """
        d = defer.Deferred()
        schema = 'octothorpe'

        def test_response(res, code=200):
            """ test event response """
            print "\n", res.request.url, res.code
            #print "\n", res.body
            self.assertEquals(res.code, code)

        d.addCallback(lambda _: self.fetch('version'))
        d.addCallback(test_response)

        d.addCallback(lambda _: self.fetch('config/default.json'))
        d.addCallback(test_response)

        d.addCallback(lambda _: self.fetch('pnml.json'))
        d.addCallback(test_response)

        d.addCallback(lambda _: self.fetch('pnml/%s.xml' % schema))
        d.addCallback(test_response)

        d.addCallback(lambda _: self.fetch('machine'))
        d.addCallback(test_response)

        d.addCallback(lambda _: self.fetch('machine/%s' % schema))
        d.addCallback(test_response)

        d.callback(None)

        return d
