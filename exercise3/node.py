from time import time
from typing import Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature

# Spróbuj zmodyfikować `DIFFICULTY` i zobacz, jak wpłynie to na czas wydobywania bloku!
DIFFICULTY = 18  # Oznacza ilość zerowych bitów na początku hasha
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
        Wykorzystaj `initial_transaction` do stworzenia blockchain (hash poprzedniego bloku i nonce powinny być zerem).
        """
        raise NotImplementedError()

    def add_transaction(self, transaction: Transaction):
        """
        TODO: Dodaj podaną transakcję do bloku.
        Sprawdź, czy transakcja jest poprawna (użyj metody `validate_transaction`), jeśli nie jest, rzuć wyjątek.
        Stwórz transakcję generującą nowego coin'a, aby wynagrodzić właściciela node'a.
        Stwórz nowy blok zawierający obie transakcje.
        Znajdź nonce, który spełni kryteria sieci (użyj metody `find_nonce`).
        Dodaj blok na koniec łańcucha.
        """
        raise NotImplementedError()

    def find_nonce(self, block: Block) -> Optional[Block]:
        """
        TODO: Znajdź nonce spełniające kryterium -> hash bloku powinien mieć na początku `DIFFICULTY` zer.
        """
        raise NotImplementedError()

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        TODO: Sprawdź poprawność transakcji.
        Transakcja jest poprawna, jeśli ma podpis, podpis jest poprawny oraz coin,
        którego chcemy wydać, istnieje i nie został wcześniej wydany.
        Skorzystaj z funkcji `verify_signature` z modułu simple_cryptography.
        """
        raise NotImplementedError()

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
    - wykonano proof of work (hash bloku ma na początku `DIFFICULTY` zer).
    """
    raise NotImplementedError()
