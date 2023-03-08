import dataclasses
from typing import List

from exercise3.block import Block


@dataclasses.dataclass
class Blockchain:
    blocks: List[Block]

    def get_latest_block(self) -> Block:
        return self.blocks[-1]

    def length(self) -> int:
        return len(self.blocks)
