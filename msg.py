"""Message communicated over peers, wrapping transaction, block, blockchain"""

import uuid as uuid_seeder


class Msg(object):
    """Packet for objects send between nodes"""
    def __init__(self, content, port):
        super(Msg, self).__init__()
        self._uuid = uuid_seeder.uuid1()
        self.content = content
        self._ports = []
        self._ports.append(port)
        self._ttl = 5

    @property
    def uuid(self):
        """Get uuid"""
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Set uuid"""
        self._uuid = uuid

    @property
    def ports(self):
        """Get list of ports"""
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Get list of ports"""
        self._ports = ports

    def visited(self, node):
        """Add node visited for this msg"""
        self.ports.append(node)

    @property
    def ttl(self):
        """Get Time-to-Live"""
        return self._ttl

    @ttl.setter
    def set_ttl(self, val):
        """Set Time-to-Live"""
        self._ttl -= val

    def elapse_ttl(self, val=1):
        """Elapse Time-to_Live"""
        self._ttl -= val
