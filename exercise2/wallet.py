import argparse
import requests
from simple_cryptography import PrivateKey, PublicKey, sign, generate_key_pair
from exercise2.transaction_registry import TransactionRegistry, Transaction
from typing import Optional, Tuple

class Wallet:
    public_key: PublicKey
    _private_key: PrivateKey

    def __init__(self, key_pair: Tuple[PublicKey, PrivateKey]):
        self.public_key = key_pair[0]
        self._private_key = key_pair[1]

    def get_unspent_transactions(self, registry: TransactionRegistry) -> list[Transaction]:
        """
        TODO: Znajdź wszystkie niewykorzystane transakcje powiązane z tym portfelem.
        Spośród wszystkich transakcji w rejestrze (registry.transactions), zwróć te z których
        każda spełnia oba warunki:
        - odbiorcą transakcji jest klucz publiczny portfela
        - transakcja nie została wykorzystana (metoda is_transaction_spent w TransactionRegistry)
        """
        wallet_transactions = filter(lambda tx: tx.recipient == self.public_key, registry.transactions)
        unspent_transactions = filter(lambda tx: not registry.is_transaction_spent(tx.tx_hash), wallet_transactions)
    
        return list(unspent_transactions)
    
    def get_balance(self, registry: TransactionRegistry) -> int:
        """
        TODO: Zwróć liczbę transakcji z wywołania get_unspent_transactions.
        """
        return len(self.get_unspent_transactions(registry))

    def transfer(self, registry: TransactionRegistry, recipient: PublicKey) -> bool:
        """
        TODO: Przekaż coina do nowego właściciela.
        - Znajdź dowolną niewykorzystaną transakcję, jeśli takiej nie ma, zwróć False.
        - Stwórz nową transakcję, z podanym odbiorcą (recipient) oraz poprzednim hashem znalezionej transakcji.
        - Podpisz nową transakcję kluczem prywatnym portfela.
        - Dodaj transakcję do rejestru.
        - Zwróć True jeśli wszystko się udało, False w przeciwnym wypadku.
        """
        unspent_transactions = self.get_unspent_transactions(registry)

        if len(unspent_transactions) == 0:
            return False

        new_transaction = Transaction(recipient, unspent_transactions[0].tx_hash)
        new_transaction.signature = sign(self._private_key, new_transaction.tx_hash)

        return registry.add_transaction(new_transaction)
