"""Miner Node"""

import copy
from time import sleep

from blockchain import Blockchain
import config
import merkle_tree

from node import Node


class MinerNode(Node):
    """ MinerNode"""
    def __init__(self, port, version, color):
        Node.__init__(self, port, version, color)
        self.blockchain = None

    def mine(self):
        """Mine a block"""
        if self.blockchain:
            trxs = self.aggregate_trxs()
            trxs_map = self.build_trxsmap(trxs)
            mtree = self.build_mtree(trxs_map.keys())
            self.blockchain.append(mtree, trxs_map)
            return True
        return False

    def seed_blockchain(self):
        """Create a genesis block and start a chain"""
        self.blockchain = Blockchain()
        from_ = to_ = self.pub_key
        amount = config.SEED_AMOUNT
        trx = self.signed_trx(from_, to_, amount, self.pri_key)
        trxs = [trx]
        trxs_map = self.build_trxsmap(trxs)
        mtree = self.build_mtree(trxs_map.keys())
        self.blockchain.seed(mtree, trxs_map)
        self.blockchain.balance_cache[str(from_.to_string())] = amount

    def aggregate_trxs(self):
        """Aggregate transactions in mempool with a set of validations"""
        trxs = []
        cbtrx = self.signed_trx(config.REWARD_KEY,
                                self.pub_key,
                                config.BLOCK_REWARD,
                                config.REWARD_PRI_KEY)
        self.blockchain.update_balance(cbtrx)
        trxs.append(cbtrx)
        new_mempool = []
        for i, trx in enumerate(self.mempool):
            if i > config.BLOCK_SIZE:
                break
            if trx.is_valid():
                if self.blockchain.validate_balance(trx):
                    self.blockchain.update_balance(trx)
                    trxs.append(trx)
                else:
                    print('Insufficient Amount Found')
                    new_mempool.append(trx)
            else:
                print('Invalid Signature Found')
        self.mempool[:] = new_mempool
        return trxs

    @staticmethod
    def build_trxsmap(trxs):
        """Build a transactions map"""
        trxs_map = {}
        for trx in trxs:
            trx_s = trx.to_string()
            trxs_map[trx_s] = trx
        return trxs_map

    @staticmethod
    def build_mtree(leaves):
        """Build merkle tree out of headers of transactions"""
        mtree = merkle_tree.MerkleTree()
        mtree.build(leaves)
        return mtree

    def routine(self):
        """Node activity routine (tx, mining, casting etc..)"""
        count = 0
        while True:
            trx = self.transfer()
            if trx:
                self.interaction.multicast_trx(trx)
            sleep(2)
            count += 1
            if count == 3:
                print('mining..')
                if self.mine():
                    print('mined. casting')
                    self.interaction.multicast_blockchain()
                count = 0
                self.status()

    def receive_trx(self, msg):
        """Receive a transaction"""
        if self.check_msg(msg):
            trx = msg.content
            if trx.is_valid():
                self.interaction.relay_trx(msg)
                trx = msg.content
                self.mempool.append(trx)
                self.msg_cache[msg.uuid] = msg

    def receive_blockchain(self, msg):
        """Receive a blockchain"""
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

    def status(self):
        """Display the status of this node"""
        if self.blockchain:
            print('')
            print('')
            print('Type: Miner')
            print('Current BC Length: {}'.format(self.blockchain.length))
            for key, value in self.blockchain.balance_cache.items():
                print('{}: {}'.format(key[:30], value))
            print('')
            print('')

    def serialize_mempool(self):
        """Serialize mempool"""
        serialized = []
        for trx in self.mempool:
            serialized.append(trx.serialize())
        return serialized

    def info(self):
        """Packing data into dictionary for rendering"""
        data = {}
        data["type"] = "Miner"
        data["pub_key"] = str(self.pub_key.to_string())
        data["mempool"] = self.serialize_mempool()
        data["blockchain"] = self.blockchain.info()
        return data
