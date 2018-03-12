"""Interactions of self.nodes"""

import json
import requests
import jsonpickle

import config
from msg import Msg

host = config.HOST


class Interaction():
    """Interaction class focus"""
    def __init__(self, node):
        self.node = node

    def bootstrap_to(self, peer_port):
        """Bootstrap to the network by connecting a peer"""
        url_to = host + ':{}/peers/'.format(peer_port)
        my_id = self.node.serialize_id(self.node.port, self.node.pub_key)
        res_id = json.loads(requests.get(url_to, json=my_id).text)
        peer_id = self.node.deserialize_id(res_id)
        if peer_id['port'] == peer_port:
            self.node.connect_to(peer_id)

    def multicast_trx(self, trx):
        """Multicast transaction"""
        for port in self.node.peers.keys():
            url_to = host + ':{}/gossip/trx/'.format(port)
            msg = jsonpickle.encode(Msg(trx, self.node.port))
            requests.post(url_to, json=json.dumps(msg))

    def multicast_blockchain(self):
        """Multicast transaction"""
        for port in self.node.peers.keys():
            url_to = host + ':{}/gossip/blockchain/'.format(port)
            msg = jsonpickle.encode(Msg(self.node.blockchain, self.node.port))
            requests.post(url_to, json=json.dumps(msg))

    def relay_trx(self, msg):
        """Relay transaction to peers"""
        for port in self.node.peers.keys():
            if port not in msg.ports:  # prevent ping-pong loop
                url_to = host + ':{}/gossip/trx/'.format(port)
                requests.post(url_to,
                              json=json.dumps(jsonpickle.encode(msg)))

    def relay_bc(self, msg):
        """Relay blockchain to peers"""
        for port in self.node.peers.keys():
            if port not in msg.ports:  # prevent ping-pong loop
                url_to = host + ':{}/gossip/blockchain/'.format(port)
                requests.post(url_to,
                              json=json.dumps(jsonpickle.encode(msg)))
