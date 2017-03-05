""" bitwrap.test.test_machine """

import json
from twisted.internet import defer
import bitwrap_io._lambda as Api
from twisted.trial.unittest import TestCase
from bitwrap_io.test import mocks

class LamdaTest(TestCase):
    """ test api methods not dealing with events"""

    def test_lambda_handler(self):
        """ test a sequence of tic-tac-toe transformations """

        res = Api.handler(mocks.API_POST, {})
        data = json.loads(res['body'])
        #print res
        self.assertTrue(data['error'] is None)

