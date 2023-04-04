from simple_cryptography import PrivateKey, PublicKey, sign
from exercise2.transaction_registry import TransactionRegistry, Transaction, SignedTransaction
from typing import Tuple, List


class Wallet:
    public_key: PublicKey

    def __init__(self, key_pair: Tuple[PublicKey, PrivateKey]):
        self.public_key = key_pair[0]

        # W produkcyjnych warunkach należy szczególnie zadbać o bezpieczeństwo klucza prywatnego.
        # W przypadku naszych warsztatów nie musimy się tym przejmować.
        self._private_key = key_pair[1]

    def get_available_transactions(self, registry: TransactionRegistry) -> List[Transaction]:
        """
        TODO: Znajdź wszystkie niewykorzystane transakcje powiązane z tym portfelem.
        Spośród wszystkich transakcji w rejestrze (registry.transactions), zwróć te z których
        każda spełnia oba warunki:
        - odbiorcą transakcji jest klucz publiczny tego portfela
        - transakcja jest niewykorzystana (metoda is_transaction_available w TransactionRegistry)
        """
        wallet_transactions = filter(lambda tx: tx.recipient == self.public_key, registry.transactions)
        available_transactions = filter(lambda tx: registry.is_transaction_available(tx.tx_hash), wallet_transactions)

        return list(available_transactions)

    def get_balance(self, registry: TransactionRegistry) -> int:
        """
        TODO: Zwróć liczbę transakcji z wywołania get_available_transactions.
        """
        return len(self.get_available_transactions(registry))

    def sign_transaction(self, transaction: Transaction) -> SignedTransaction:
        """
        TODO: Podpisz transakcję kluczem prywatnym.
        Korzystając z funkcji sign z simple_cryptography, stwórz podpis danej transakcji.
        Następnie zwróc podpisaną transakcję jako obiekt klasy SignedTransaction.
        """
        signature = sign(self._private_key, transaction.tx_hash)
        return SignedTransaction.from_transaction(transaction, signature)

    def transfer(self, registry: TransactionRegistry, recipient: PublicKey) -> bool:
        """
        TODO: Przekaż coina do nowego właściciela.
        - Znajdź dowolną niewykorzystaną transakcję, jeśli takiej nie ma, zwróć False.
        - Stwórz nową transakcję, z podanym odbiorcą (recipient) oraz poprzednim hashem znalezionej transakcji.
        - Podpisz nową transakcję korzystając z sign_transaction.
        - Dodaj transakcję do rejestru.
        - Zwróć True jeśli wszystko się udało, False w przeciwnym wypadku.
        """
        available_transactions = self.get_available_transactions(registry)

        if len(available_transactions) == 0:
            return False

        new_transaction = Transaction(recipient, available_transactions[0].tx_hash)
        signed_transaction = self.sign_transaction(new_transaction)

        return registry.add_transaction(signed_transaction)
