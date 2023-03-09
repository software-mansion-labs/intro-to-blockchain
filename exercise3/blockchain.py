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
        TODO: Zwróć ostatni blok.
        """
        raise NotImplementedError()

    def length(self) -> int:
        """
        TODO: Zwróć długość łańcucha.
        """
        raise NotImplementedError()

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        """
        TODO: Przy pomocy podanego `tx_hash` wyszukaj transakcję.
        """
        raise NotImplementedError()

    def get_transaction_by_previous_tx_hash(
        self, previous_tx_hash: bytes
    ) -> Optional[Transaction]:
        """
        TODO: Przy pomocy podanego `previous_tx_hash` wyszukaj transakcję.
        """
        raise NotImplementedError()
