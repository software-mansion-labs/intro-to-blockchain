from dataclasses import dataclass
from typing import List

from exercise1.hash_1 import Transaction
from simple_cryptography import hash


@dataclass
class Block:
    prev_block_hash: bytes
    timestamp: int
    nonce: int
    transactions: List[Transaction]

    @property
    def hash(self):
        hashed_txs = b'\x00'
        for tx in self.transactions:
            hashed_txs = hash(hashed_txs + tx.hash())

        return hash(self.prev_block_hash +
                    self.timestamp.to_bytes(32, 'big') +
                    self.nonce.to_bytes(32, 'big') +
                    hashed_txs)
