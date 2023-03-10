# Funkcje hashujące

from dataclasses import dataclass
from simple_cryptography import hash


@dataclass
class Transaction:
    id: int
    target_id: int
    metadata: str


    def hash(self) -> bytes:
        """
        TODO -- zaimplementuj funckję hashującą transakcje wykorzystując funkcję hash z simple_cryptography
        wykorzystaj metodę int.to_bytes(2, 'big') oraz bytes(string, 'utf-8') do konwersji int to bytes
        bytes mozna konkatenować
        """
        hash(int.to_bytes(self.id, 2, 'big') + int.to_bytes(self.id, 2, 'big') + bytes(self.metadata, 'utf-8'))