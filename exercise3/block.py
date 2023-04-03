from typing import List

from exercise2.transaction_registry import Transaction
from simple_cryptography import hash


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

    def __init__(
        self, prev_block_hash: bytes, transactions: List[Transaction], nonce: int = 0
    ):
        """
        TODO: Stwórz blok z podanych argumentów.
        Aby pobrać aktualny czas, użyj funkcji time(), a następnie zrzutuj ją na int'a ( int(time()) ).
        """
        raise NotImplementedError()

    def hash(self):
        """
        TODO: Oblicz hash bloku wykorzystując do tego funkcję `hash` z modułu simple_cryptography.
        Hash powinien składać się z wszystkich składowych bloku:
        - prev_block_hash
        - timestamp
        - nonce
        - hasha wszystkich transakcji:
            - stwórz zmienną reprezentującą hash wszystkich transakcji (zainicjalizowaną bajtem zerowym b'0')
            - przechodząc po wszystkich transakcjach
            - zaktualizuj hash wszystkich transakcji, hashem aktualnej
             all_tx_hash = hash(all_tx_hash + current_tx_hash)
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
