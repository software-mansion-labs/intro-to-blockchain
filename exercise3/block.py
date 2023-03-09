from dataclasses import dataclass
from typing import List

from exercise2.transaction_registry import Transaction
from simple_cryptography import hash


@dataclass
class Block:
    """
    Blok powinien zawierać:
    - hash poprzedniego bloku,
    - moment w czasie, w którym został stworzony,
    - listę transakcji
    - nonce.
    """

    prev_block_hash: bytes
    timestamp: int
    nonce: int
    transactions: List[Transaction]

    @property
    def hash(self):
        """
        TODO: Oblicz hash bloku wykorzystując do tego funkcję `hash` z modułu simple_cryptography.
        Hash powinien zawierać wszystkie składowe bloku.
        """
        hashed_txs = b"\x00"
        for transaction in self.transactions:
            hashed_txs = hash(hashed_txs + transaction.tx_hash)

        return hash(
            self.prev_block_hash
            + self.timestamp.to_bytes(32, "big")
            + self.nonce.to_bytes(32, "big")
            + hashed_txs
        )
