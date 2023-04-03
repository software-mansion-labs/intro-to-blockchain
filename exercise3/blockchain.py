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

    def get_transaction_by(
        self, tx_hash: Optional[bytes] = None, previous_tx_hash: Optional[bytes] = None
    ) -> Optional[Transaction]:
        """
        TODO: Przy pomocy podanego argumentu wyszukaj transakcję.
        Można podać tylko jeden z dwóch argumentów. W zależności od tego, który został podany,
        użyj go do znalezienia transakcji.
        """
        raise NotImplementedError()
