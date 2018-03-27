"""Configurations of this crypto"""

from key import Key


HOST = 'http://localhost'

BLOCK_TIME = 100  # sec
BLOCK_SIZE = 10
BLOCK_REWARD = 300
TRANSACTION_INTERVAL = 5  # sec
SEED_AMOUNT = 1000
VERSION = 1

KEY = Key()
REWARD_KEY = KEY.public_key
REWARD_KEY_S = str(REWARD_KEY.to_string())
REWARD_PRI_KEY = KEY.private_key
