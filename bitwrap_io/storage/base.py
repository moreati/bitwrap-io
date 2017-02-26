import ujson as json

class Storage(object):

    @staticmethod
    def encode_key(input_str):
        """ make sure keys are safe for lmdb """
        return input_str.encode('latin-1')

    @staticmethod
    def serialize(val):
        """ unserialize json from lmdb """
        return json.dumps(val)

    @staticmethod
    def unserialize(val):
        """ unserialize json from lmdb """
        if val is None:
            return None
        else:
            return json.loads(val)
