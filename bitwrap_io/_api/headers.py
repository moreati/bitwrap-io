""" share headers accross resources """
import os

_ALLOW = os.environ.get('ALLOW_ORIGIN', '*')

class Mixin(object):
    """ set default api headers """

    def options(self):
        """ allow cors """
        pass

    def set_default_headers(self):
        """ allow cors """
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', _ALLOW)
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.set_header('Access-Control-Allow-Methods', 'GET')
