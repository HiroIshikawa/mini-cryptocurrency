"""Proof of Work"""

import random
import sys
from hashlib import sha256


class PoW():
    """Proof of Work"""
    def __init__(self, difficulty=5):
        self._difficulty = difficulty
        self.timelimit = None

    @staticmethod
    def _count_leading_zeros(word):
        """Count the number of leading zeros"""
        i = 0
        while word[i] == '0':
            i += 1
        return i

    def mint(self, challenge):
        """Generate nonce"""
        while True:
            nonce = random.randint(0, sys.maxsize)
            work = sha256((str(challenge)+str(nonce)).encode()).hexdigest()
            leading_zeros = self._count_leading_zeros(work)
            if leading_zeros >= self.difficulty:
                return nonce

    @property
    def difficulty(self):
        """Get difficulty of this PoW"""
        return self._difficulty

    @difficulty.setter
    def difficulty(self, dif):
        """Set difficulty of this PoW"""
        self._difficulty = dif
