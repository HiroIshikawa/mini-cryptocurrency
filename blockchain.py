"""Blockchain"""

from hashlib import sha256

import config
from block import Block


class Blockchain():
    """Blockchain"""
    def __init__(self):
        self.blockchain = []
        self._length = 0
        self.balance_cache = {}

    @property
    def length(self):
        """Get length of this blockchain"""
        return self._length

    @length.setter
    def length(self, new_len):
        """Set length of this blockchain"""
        self._length = new_len

    def seed(self, mtree, trxs_map):
        """Seed a blockchain"""
        prev_hash = 'This is the genesis block.'
        seed_block = Block(prev_hash, mtree.root.value, mtree, trxs_map)
        self.blockchain.append(seed_block)
        self.length += 1

    def append(self, mtree, trxs_map):
        """Append a block"""
        prev_block = self.blockchain[-1]
        prev_hash = prev_block.to_hash()
        new_block = Block(prev_hash, mtree.root.value, mtree, trxs_map)
        self.blockchain.append(new_block)
        self.length += 1

    def update_balance(self, trx):
        """Update the balance in this blockchain"""
        if trx.from_s != config.REWARD_KEY_S:
            self.balance_cache[trx.from_s] -= trx.amount
        if trx.to_s in self.balance_cache:
            self.balance_cache[trx.to_s] += trx.amount
        else:
            self.balance_cache[trx.to_s] = trx.amount

    def count_balance(self):
        """Count the balance to validate"""
        temp_balance = {}
        for block in self.blockchain:
            for trx in block.trxs_map.values():
                if trx.from_s != config.REWARD_KEY_S:
                    temp_balance[trx.from_s] -= trx.amount
                if trx.to_s in temp_balance:
                    temp_balance[trx.to_s] += trx.amount
                else:
                    temp_balance[trx.to_s] = trx.amount
        return temp_balance

    def validate_balance(self, trx):
        """Validate a transaction with sufficient balance"""
        if self.balance_cache:
            if trx.from_s in self.balance_cache:
                if (self.balance_cache[trx.from_s] - trx.amount) >= 0:
                    return True
        return False

    def has_valid_chain(self):
        """Validate the prev hash values"""
        for i, block in enumerate(self.blockchain[1:]):
            prev_block = self.blockchain[i]
            if prev_block.to_hash() != block.prev_hash:
                return False
        return True

    def is_valid(self):
        """Validate blockchain"""
        print('start validating')
        for block in self.blockchain:
            if not block.has_valid_sigs():
                return False
            print('sigs validation complete')
        # validate chain
        if not self.has_valid_chain():
            return False
        return True

    def list(self):
        """List blockchain values"""
        return [(str(el.version), el.prev_hash, el.nonce,
                 sha256((el.challenge()+str(el.nonce)).encode()).hexdigest())
                for el in self.blockchain]

    def info(self):
        """Pack blockchain info to get rendered"""
        data = {}
        data['length'] = self.length
        data['blocks'] = []
        for block in self.blockchain:
            data['blocks'].append(block.info())
        return data
