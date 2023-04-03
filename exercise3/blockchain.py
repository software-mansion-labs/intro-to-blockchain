from typing import List, Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block


class Blockchain:
    """
    Klasa reprezentująca łańcuch bloków.
    Powinna zawierać:
    - listę bloków.
    """

    blocks: List[Block]

    def __init__(self, initial_transaction: Transaction):
        initial_block = Block(
            prev_block_hash=b"\x00", transactions=[initial_transaction], nonce=0
        )
        self.blocks = [initial_block]

    def get_latest_block(self) -> Block:
        """
        TODO: Zwróć ostatni blok.
        """
        return self.blocks[-1]

    def length(self) -> int:
        """
        TODO: Zwróć długość łańcucha.
        """
        return len(self.blocks)

    def get_transaction_by(
        self, tx_hash: Optional[bytes] = None, previous_tx_hash: Optional[bytes] = None
    ) -> Optional[Transaction]:
        """
        TODO: Przy pomocy podanego argumentu wyszukaj transakcję.
        Można podać tylko jeden z dwóch argumentów.
        W zależności od tego, który został podany, użyj go do znalezienia transakcji.
        Przechodząc po wszystkich blokach i ich transakcjach zwróć pasującą transakcję.
        """
        if tx_hash is not None and previous_tx_hash is not None:
            raise Exception(
                "Arguments tx_hash and previous_tx_hash are mutually exclusive."
            )

        for block in self.blocks:
            for transaction in block.transactions:
                if (
                    tx_hash is not None
                    and transaction.tx_hash == tx_hash
                    or previous_tx_hash is not None
                    and transaction.previous_tx_hash == previous_tx_hash
                ):
                    return transaction

        return None
