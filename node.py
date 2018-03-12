"""Node"""

import json
import random
from ecdsa import VerifyingKey

from key import Key
from transaction import Transaction
from interaction import Interaction


class Node():
    """Generic node class"""
    def __init__(self, port, version, color):
        key = Key()
        self.pri_key = key.private_key
        self.pub_key = key.public_key
        self.port = port
        self.version = version
        self.color = color
        self.peers = {}
        self.mempool = []
        self.msg_cache = {}
        self.interaction = Interaction(self)

    def connect_to(self, peer):
        """Connect to peer"""
        self.peers[peer['port']] = peer['pub_key']

    def disconnect_from(self, peer_port):
        """"Disconnect from peer"""
        if peer_port in self.peers:
            self.peers.pop(peer_port, None)

    def signed_trx(self, from_, to_, amount, pri_key):
        """Generate signed transaction"""
        trx = Transaction(from_, to_, amount)
        trx.sign(pri_key)
        return trx

    def transfer(self, from_=None, to_=None, amount=None):
        """Transfer a value to self/random peer"""
        if from_ is None and to_ is None and amount is None:
            amount = random.randint(100, 700)
            from_ = self.pub_key
            if self.peers:
                peer_port = random.choice(list(self.peers.keys()))
                to_ = self.peers[peer_port]
            else:
                to_ = self.pub_key
        trx = self.signed_trx(from_, to_, amount, self.pri_key)
        self.mempool.append(trx)
        return trx

    def check_msg(self, msg):
        """Check message"""
        msg.elapse_ttl()
        msg.visited(self.port)
        return msg.ttl > 0 and msg.uuid not in self.msg_cache

    def receive_trx(self, msg):
        """Receive transaction"""
        raise NotImplementedError

    def receive_blockchain(self, msg):
        """Receive a blockchain"""
        raise NotImplementedError

    @staticmethod
    def serialize_id(port, pub_key):
        """Serialize id"""
        return json.dumps(
            {'port': port,
             'pub_key': pub_key.to_pem().decode('utf-8', 'ignore')})

    @staticmethod
    def deserialize_id(id_):
        """Deserialize id"""
        id_['pub_key'] = VerifyingKey.from_pem(
            id_['pub_key'].encode('utf-8', 'ignore'))
        return id_

    def routine(self):
        """Routine in auto simulation"""
        raise NotImplementedError

    def status(self):
        """Display node's status"""
        raise NotImplementedError

    def info(self):
        """Packing data into dictionary for rendering"""
        raise NotImplementedError
