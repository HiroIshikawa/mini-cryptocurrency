"""SPV Node"""

from time import sleep

from node import Node


class SPVNode(Node):
    """SPVNode"""
    def __init__(self, port, version, color):
        Node.__init__(self, port, version, color)

    def receive_trx(self, msg):
        """Receive a transaction"""
        self.interaction.relay_trx(msg)
        self.msg_cache[msg.uuid] = msg

    def receive_blockchain(self, msg):
        """Receive a blockchain"""
        self.interaction.relay_bc(msg)
        self.msg_cache[msg.uuid] = msg

    def routine(self):
        """SPVNode routine"""
        while True:
            trx = self.transfer()
            if trx:
                self.interaction.multicast_trx(trx)
            sleep(2)
            self.status(trx)

    def status(self, trx):
        """Display status"""
        print('')
        print('')
        print('Type: SPV')
        print('Recent transaction')
        print(trx)
        print('')
        print('')

    def info(self):
        """Packing data into dictionary for rendering"""
        data = {}
        data["type"] = "SPV"
        data["pub_key"] = str(self.pub_key.to_string())
        data["mempool"] = self.mempool
        return data
