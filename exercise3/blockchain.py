import dataclasses
from typing import List, Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block


@dataclasses.dataclass
class Blockchain:
    blocks: List[Block]

    def get_latest_block(self) -> Block:
        return self.blocks[-1]

    def length(self) -> int:
        return len(self.blocks)

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.tx_hash == tx_hash:
                    return transaction

        return None
