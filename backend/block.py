"""Block"""

from hashlib import sha256

import config
from prow import PoW


class Block():
    """Block"""
    def __init__(self, prev_hash, merkleroot_hash, mtree, trxs_map):
        self.version = config.VERSION
        self.prev_hash = prev_hash
        self.merkleroot_hash = merkleroot_hash
        challenge = self.to_challenge()
        self.nonce = PoW().mint(challenge)
        self.mtree = mtree
        self.trxs_map = trxs_map

    def has_valid_sigs(self):
        """Check all sigs in trxs"""
        for trx in self.trxs_map.values():
            if not trx.is_valid():
                return False
        return True

    def to_challenge(self):
        """Generate challenge for pow"""
        return str(self.version)+self.prev_hash+self.merkleroot_hash

    def to_hash(self):
        """Generate hash of this block"""
        data = (self.to_challenge()+str(self.nonce)).encode()
        return sha256(sha256(data).hexdigest().encode()).hexdigest()

    def serialize_trxs(self):
        """Serialize transactions"""
        serialized = {}
        for key, val in self.trxs_map.items():
            serialized[str(key)] = val.serialize()
        return serialized

    def info(self):
        """Pack block info to get rendered"""
        data = {}
        data['prev_hash'] = self.prev_hash
        data['merkleroot_hash'] = self.merkleroot_hash
        data['nonce'] = self.nonce
        data['trxs_map'] = self.serialize_trxs()
        return data
