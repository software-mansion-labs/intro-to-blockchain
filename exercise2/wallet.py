from simple_cryptography import PrivateKey, PublicKey
from exercise2.transaction_registry import (
    TransactionRegistry,
    Transaction,
)
from typing import Tuple, List


class Wallet:
    public_key: PublicKey

    def __init__(self, key_pair: Tuple[PublicKey, PrivateKey]):
        self.public_key = key_pair[0]

        # W produkcyjnych warunkach należy szczególnie zadbać o bezpieczeństwo klucza prywatnego.
        # W przypadku naszych warsztatów nie musimy się tym przejmować.
        self._private_key = key_pair[1]

    def get_available_transactions(
        self, registry: TransactionRegistry
    ) -> List[Transaction]:
        """
        TODO: Znajdź wszystkie niewykorzystane transakcje powiązane z tym portfelem.
        Spośród wszystkich transakcji w rejestrze (registry.transactions), zwróć te z których
        każda spełnia oba warunki:
        - odbiorcą transakcji jest klucz publiczny tego portfela
        - transakcja jest niewykorzystana (metoda is_transaction_available w TransactionRegistry)
        """
        raise NotImplementedError()

    def get_balance(self, registry: TransactionRegistry) -> int:
        """
        TODO: Zwróć liczbę transakcji z wywołania get_available_transactions.
        """
        raise NotImplementedError()

    def transfer(self, registry: TransactionRegistry, recipient: PublicKey) -> bool:
        """
        TODO: Przekaż coina do nowego właściciela.
        1.  Znajdź dowolną niewykorzystaną transakcję dla tego portfela, jeśli takiej nie ma, zwróć False.
        2.  Stwórz nową transakcję, z podanym odbiorcą (recipient) oraz polem previous_tx_hash ustawionym na
            tx_hash znalezionej transakcji.
        3.  Podpisz nową transakcję korzystając z Transaction::sign.
        4.  Dodaj transakcję do rejestru.
        5.  Zwróć True jeśli wszystko się udało, False w przeciwnym wypadku. (Pamiętaj że add_transaction też zwraca
            True lub False w zależności od powodzenia)
        """
        raise NotImplementedError()
