"""Full Node"""

import copy
from time import sleep

from node import Node


class FullNode(Node):
    """FullNode"""
    def __init__(self, port, version, color):
        Node.__init__(self, port, version, color)
        self.blockchain = None

    def receive_trx(self, msg):
        """Receive a transaction"""
        if self.check_msg(msg):
            trx = msg.content
            if trx.is_valid():
                self.interaction.relay_trx(msg)
                self.msg_cache[msg.uuid] = msg

    def receive_blockchain(self, msg):
        """Receive blockchain"""
        if self.check_msg(msg):
            new_blockchain = msg.content
            if new_blockchain.is_valid():
                self.interaction.relay_bc(msg)
                if self.blockchain:
                    if new_blockchain.length > self.blockchain.length:
                        self.blockchain = copy.copy(new_blockchain)
                else:
                    self.blockchain = copy.copy(new_blockchain)
                self.msg_cache[msg.uuid] = msg

    def routine(self):
        """Fullnode routine"""
        while True:
            trx = self.transfer()
            if trx:
                self.interaction.multicast_trx(trx)
            sleep(2)
            self.status(trx)

    def status(self, trx):
        """Display status of this node"""
        print('')
        print('')
        print('Type: Full')
        print('Recent Transaction')
        print(trx)
        if self.blockchain:
            print('Current BC Length: {}'.format(self.blockchain.length))
            for key, value in self.blockchain.balance_cache.items():
                print('{}: {}'.format(key[:30], value))
        print('')
        print('')

    def info(self):
        """Packing data into dictionary for rendering"""
        data = {}
        data["type"] = "Full"
        data["pub_key"] = str(self.pub_key.to_string())
        data["mempool"] = self.mempool
        if self.blockchain:
            data["blockchain"] = self.blockchain.info()
        return data
