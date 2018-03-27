"""Merkle tree"""

import hashlib


class ProofNode():
    """Node for Merkle Proof"""
    def __init__(self, value, left_or_right):
        self.value = value
        self.left_or_right = left_or_right

    def __repr__(self):
        return '{}: {}...'.format(self.left_or_right, self.value[:20])


class Node():
    """Node for Merkle Tree Construction"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class MerkleTree():
    """Merkle Tree"""
    def __init__(self, padding_key=''):
        self.root = None
        self.padding_key = padding_key

    def build(self, blocks):
        """Build Merkle Tree"""
        blocks = self._add_paddings(blocks, self.padding_key)
        if not len(blocks) // 2:
            self.padding(blocks)
        blocks = [Node(self.hashing(block)) for block in blocks]
        while len(blocks) > 1:
            left = blocks.pop(0)
            right = blocks.pop(0)
            parent = Node(self.hashing(left.value+right.value), left, right)
            blocks.append(parent)
        self.root = parent

    def traverse(self):
        """Traverse Tree"""
        node = self.root
        self.traverse_helper(node)

    def traverse_helper(self, node):
        """Helper for traverse"""
        if node is None:
            return
        self.traverse_helper(node.left)
        self.traverse_helper(node.right)
        print(node.value)

    def generate_proof(self, block):
        """Generate Merkle Proof"""
        result = []
        target = self.hashing(block)
        root = self.root
        hit = []
        self._generate_proof_helper(root, target, hit, result)
        print('Generated Proof:', result)
        return result

    def _generate_proof_helper(self, root, target, hit, result):
        """Helper to generate Merkle Proof"""
        if root is None:
            return
        if root.value == target:
            hit.append('hit')
            return
        if not hit:
            self._generate_proof_helper(root.left, target, hit, result)
        if hit:
            result.append(ProofNode(root.right.value, 'r'))
            return
        if not hit:
            self._generate_proof_helper(root.right, target, hit, result)
        if hit:
            result.append(ProofNode(root.left.value, 'l'))
            return

    def verify_proof(self, block, proof):
        """Verify Merkle Proof"""
        cur_hash = ''
        for i, pnode in enumerate(proof):
            if i == 0:
                if pnode.left_or_right == 'r':
                    cur_hash = self.hashing(self.hashing(block)+pnode.value)
                else:
                    cur_hash = self.hashing(pnode.value+self.hashing(block))
            else:
                if pnode.left_or_right == 'r':
                    cur_hash = self.hashing(cur_hash+pnode.value)
                else:
                    cur_hash = self.hashing(pnode.value+cur_hash)
        return cur_hash == self.root.value

    def _add_paddings(self, blocks, padding):
        """Add padding for leaf nodes"""
        return [padding.encode()+el for el in blocks]

    def padding(self, blocks):
        """Add padding to a leave nodes"""
        blocks.append(self.padding_key)

    def hashing(self, s):
        """Hash string"""
        if type(s) == str:
            return hashlib.sha256(s.encode()).hexdigest()
        return hashlib.sha256(s).hexdigest()

# ---- Mini Test
# if __name__ == '__main__':
#     blocks = [b"We", b"hold", b"these", b"truths",
#               b"to", b"be", b"self-evident", b"that"]
#     # mempool = mempool_sample()
#     # txs = []
#     # for tx_hash, tx in mempool.items():
#     #     txs.append(tx_hash, tx)
#     MT = MerkleTree()
#     MT.build(blocks.copy())
#     for block in blocks:
#         proof = MT.generate_proof(block)
#         if MT.verify_proof(block, proof):
#             print("{} proven".format(block))
#             print()
