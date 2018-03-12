"""Key"""

from ecdsa import SigningKey
import ecdsa


class Key():
    """Key pair"""
    def __init__(self):
        self.sk = SigningKey.generate(curve=ecdsa.SECP256k1)
        self.vk = self.sk.get_verifying_key()

    @property
    def private_key(self):
        return self.sk

    @property
    def public_key(self):
        return self.vk
