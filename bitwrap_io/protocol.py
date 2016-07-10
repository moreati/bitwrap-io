import json
from twisted.protocols.basic import LineOnlyReceiver
from twisted.protocols.policies import TimeoutMixin
from twisted.python import failure
from twisted.internet import error

class BitwrapStreamingProtocol(LineOnlyReceiver, TimeoutMixin):
    def __init__(self, receiver, stream, timeout_seconds=60):
        self.receiver = receiver
        self.stream = stream
        self.setTimeout(timeout_seconds)

    def lineReceived(self, line):
        self.resetTimeout()
        line = line.strip()
        if line:
            try:
                obj = json.loads(line)
                if 'text' in obj:
                    self.receiver.status(obj)
                elif 'delete' in obj:
                    self.receiver.status_deletion(obj)
                elif 'scrub_geo' in obj:
                    self.receiver.location_deletion(obj)
                elif 'limit' in obj:
                    self.receiver.rate_limitation(obj)
                else:
                    self.receiver.json(obj)
            except ValueError, e:
                print e
                self.receiver.invalid(line)

    def connectionLost(self, reason):
        self.stream.disconnect(reason)
        self.receiver.disconnected(reason)

    def timeoutConnection(self):
        self.stream.disconnect(failure.Failure(error.ConnectionLost()))
        self.receiver.disconnected(failure.Failure(error.ConnectionLost()))
