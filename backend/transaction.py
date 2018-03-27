"""Transaction"""

import hashlib


class Transaction():
    """Transaction"""
    def __init__(self, from_, to_, amount):
        self.from_ = from_  # pubkey: can decrypt
        self.to_ = to_  # pubkey: can decrypt
        self.amount = amount
        self.signature = None  # with private key to encrypt

    @property
    def from_s(self):
        """Get string of the sender's key"""
        return str(self.from_.to_string())

    @property
    def to_s(self):
        """Get string of the recepient's key"""
        return str(self.to_.to_string())

    def to_string(self):
        """Stringfy the summary of this transaction"""
        return self.from_.to_string()+self.to_.to_string()+bytes(self.amount)

    def hash(self):
        """Make a hash for the stringified summary of this transaction"""
        tx_str = self.to_string()
        return hashlib.sha256(tx_str).hexdigest().encode()

    def sign(self, pri_key):
        """Sign this transaction with owner's private key"""
        self.signature = pri_key.sign(self.hash(),
                                      hashfunc=hashlib.sha1)

    def serialize(self):
        """Serialize transactions"""
        serialized = {}
        serialized['from'] = self.from_s
        serialized['to'] = self.to_s
        serialized['amount'] = str(self.amount)
        return serialized

    def is_valid(self):
        """Verify the transaction with sender's sign and hash"""
        return self.from_.verify(self.signature,
                                 self.hash(),
                                 hashfunc=hashlib.sha1)

    def __repr__(self):
        return '{} to {}: {}'.format(self.from_.to_string()[:8],
                                     self.to_.to_string()[:8],
                                     self.amount)
