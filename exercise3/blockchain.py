import dataclasses
from typing import List, Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block


@dataclasses.dataclass
class Blockchain:
    """
    Klasa reprezentująca łańcuch bloków.
    Powinna zawierać:
    - listę bloków.
    """
    blocks: List[Block]

    def get_latest_block(self) -> Block:
        """
        Zwróć ostatni blok.
        """
        return self.blocks[-1]

    def length(self) -> int:
        """
        Zwróć długość łańcucha.
        """
        return len(self.blocks)

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        """
        Przy pomocy podanego `tx_hash` wyszukaj transakcję.
        """
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.tx_hash == tx_hash:
                    return transaction

        return None
