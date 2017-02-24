#!/usr/bin/env python

import os
from twisted.application import service, internet
from twisted.internet.protocol import Factory
from bitwrap_io.api import factory as ApiFactory

Factory.noisy = False

application = service.Application("bitwrap-io")

internet.TCPServer(
    int(os.environ.get('BITWRAP_PORT', 8080)),
    ApiFactory(),
    interface=os.environ.get('BITWRAP_IFACE', "0.0.0.0")
).setServiceParent(application)

