from time import time
from typing import Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature, generate_key_pair

# Spróbuj zmodyfikować `DIFFICULTY` i zobacz, jak wpłynie to na czas wydobywania bloku!
DIFFICULTY = 10  # Oznacza ilość zerowych bitów na początku hasha
MAX_256_INT = 2**256


class Node:
    """
    Klasa reprezentująca węzeł sieci. Odpowiada za dodawanie transakcji i tworzenie bloków.
    Powinna zawierać:
    - blockchain,
    - klucz publiczny właściciela, wykorzystywany do przypisywania nowych coin'ów do konta.
    """

    blockchain: Blockchain
    owner: PublicKey

    def __init__(self, owner_public_key: PublicKey, initial_transaction: Transaction):
        """
        TODO: Przypisz wartości polom owner oraz blockchain przy pomocy podanych argumentów.
        Wykorzystaj `initial_transaction` do stworzenia blockchain.
        """
        self.owner = owner_public_key
        self.blockchain = Blockchain(initial_transaction)

    def validate_transaction(self, transaction: SignedTransaction) -> bool:
        """
        TODO: Sprawdź poprawność transakcji.
        Transakcja jest poprawna, jeśli:
        - ma podpis,
        - podpis jest poprawny
        - coin (transakcja), którego chcemy wydać, istnieje i nie został wcześniej wydany.

        Do weryfikacji podpisu skorzystaj z funkcji `verify_signature` z modułu simple_cryptography.

        Jak sprawdzić, czy coin istnieje?
        Spróbuj znaleźć transakcję, o hashu takim samym jak hash transakcji, którą chcemy wydać.

        Jak sprawdzić, czy coin nie został wcześniej wydany?
        Spróbuj znaleźć transakcję, której previous_tx_hash jest taki sam, jak hash transakcji, którą chcemy wydać.

        !! Ważne !!
        Transakcja, którą chcemy wydać oznacza transakcję poprzednią do tej podanej w argumencie `transaction`.
        """
        if transaction.signature is None:
            return False

        prev_transaction = self.blockchain.get_transaction_by(
            tx_hash=transaction.previous_tx_hash
        )
        if prev_transaction is None:
            return False

        if (
            self.blockchain.get_transaction_by(
                previous_tx_hash=prev_transaction.tx_hash
            )
            is not None
        ):
            return False

        return verify_signature(
            prev_transaction.recipient, transaction.signature, transaction.tx_hash
        )

    def find_nonce(self, block: Block) -> Optional[Block]:
        """
        TODO: Znajdź nonce spełniające kryterium -> hash bloku powinien mieć na początku `DIFFICULTY` zer.

        Jak sprawdzić ilość zer na początku hasha?
        Porównaj hash zrzutowany na int oraz maksymalną wartość inta 256 przesuniętą bitowo o DIFFICULTY.

        Przydatne operacje:
        - int.from_bytes(hash, "big")
        - MAX_256_INT >> DIFFICULTY
        """
        while int.from_bytes(block.hash(), "big") > MAX_256_INT >> DIFFICULTY:
            block.nonce += 1
        return block

    def add_transaction(self, transaction: Transaction):
        """
        TODO: Dodaj podaną transakcję do bloku.
        Sprawdź, czy transakcja jest poprawna (użyj metody `validate_transaction`), jeśli nie jest, rzuć wyjątek.
        Stwórz transakcję generującą nowego coin'a, aby wynagrodzić właściciela node'a.
        Stwórz nowy blok zawierający obie transakcje.
        Znajdź nonce, który spełni kryteria sieci (użyj metody `find_nonce`).
        Dodaj blok na koniec łańcucha.
        """
        if not self.validate_transaction(transaction):
            raise Exception("Transaction can't be added. Verification failed.")

        new_coin_transaction = Transaction(
            recipient=self.owner, previous_tx_hash=b"\x00"
        )
        new_block = Block(
            prev_block_hash=self.blockchain.get_latest_block().hash(),
            nonce=0,
            transactions=[transaction, new_coin_transaction],
        )

        new_block = self.find_nonce(new_block)
        self.blockchain.blocks.append(new_block)

    def get_state(self) -> Blockchain:
        """
        Zwróć blockchain.
        """
        return self.blockchain


def validate_chain(chain: Blockchain) -> bool:
    """
    TODO: Zweryfikuj poprawność łańcucha.
    Łańcuch jest poprawny, jeśli dla każdego bloku (poza zerowym):
    - hash poprzedniego bloku jest przypisany prawidłowo,
    _ timestamp rośnie razem z numerem bloku,
    - wykonano proof of work (hash bloku ma na początku `DIFFICULTY` zer),
    - wszystkie transakcje w bloku są poprawne.

    Pamiętaj, że w bloku istnieją transakcje tworzące nowe coiny! (nie będą miały one podpisu)
    """
    if len(chain.blocks[0].transactions) != 1:
        return False

    honest_node = Node(generate_key_pair()[0], chain.blocks[0].transactions[0])

    for index, block in enumerate(chain.blocks[1:]):
        if block.prev_block_hash != chain.blocks[index].hash():
            return False

        if block.timestamp < chain.blocks[index].timestamp:
            return False

        if int.from_bytes(block.hash(), "big") > MAX_256_INT >> DIFFICULTY:
            return False

        new_coin_transaction_used = False
        for transaction in block.transactions:
            if transaction.previous_tx_hash == b"\00":
                if new_coin_transaction_used:
                    return False
                new_coin_transaction_used = True
                continue

            if not honest_node.validate_transaction(transaction):
                return False

        honest_node.blockchain.blocks.append(block)

    return True
