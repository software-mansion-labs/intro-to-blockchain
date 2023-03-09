from simple_cryptography import hash, PublicKey, verify_signature
from dataclasses import dataclass
from typing import Optional, List
import copy

@dataclass
class Transaction:
    """
    Transakcja zawiera:
    - odbiorcę transakcji (klucz publiczny)
    - hash poprzedniej transakcji
    """
    recipient: PublicKey    
    previous_tx_hash: bytes

    @property
    def tx_hash(self):
        return hash(self.recipient.to_bytes() + self.previous_tx_hash)

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes):
        self.recipient = recipient
        self.previous_tx_hash = previous_tx_hash
    
    def __repr__(self):
        return f"Tx(recipient: {self.recipient.to_bytes()[8:14]}.., prev_hash: {self.previous_tx_hash[:6]}..)"

@dataclass
class SignedTransaction(Transaction):
    """
    Podpisana transakcja zawiera dodatkowo:
    - Podpis transakcji, utworzony przy pomocy klucza prywatnego poprzedniego właściciela transakcji.
    """
    signature: bytes

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes, signature: bytes):
        super().__init__(recipient, previous_tx_hash)
        self.signature = signature
    
    def __init__(self, transaction: Transaction, signature: bytes):
        super().__init__(transaction.recipient, transaction.previous_tx_hash)
        self.signature = signature

class TransactionRegistry:
    """
    Klasa reprezentująca publiczny rejestr transakcji. Odpowiada za przyjmowanie nowych transakcji i ich
    przechowywanie.
    """
    transactions: List[Transaction]

    def __init__(self, initial_transactions: List[Transaction]):
        self.transactions = copy.copy(initial_transactions)

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        """
        TODO: Znajdź transakcję z podanym tx_hash.
        Jeśli istnieje transakcja z podanym tx_hash, zwróć ją, w przeciwnym przypadku zwróć None.
        """
        for tx in self.transactions:
            if tx.tx_hash == tx_hash:
                return tx    
        
        return None

    def is_transaction_spent(self, tx_hash: bytes) -> bool:
        """
        TODO: Sprawdź czy transakcja o podanym hashu została wykorzystana.
        Tj. sprawdź czy istnieje inna transakcja dla której ta transakcja jest
        wcześniejszą transakcją. (pole previous_tx_hash).
        """
        for tx in self.transactions:
            if tx.previous_tx_hash == tx_hash:
                return True
        
        return False

    def verify_transaction_signature(self, transaction: Transaction) -> bool:
        """
        TODO: Zweryfikuj podpis transakcji. 
        Sprawdź czy dana transakcja została podpisana przez właściciela (klucz publiczny) poprzedniej transakcji.
        Do weryfikacji podpisu wykorzystaj funkcję verify_signature z simple_cryptography.
        Przypomnienie: podpisywany jest hash transakcji.
        """
        previous_transaction = self.get_transaction(transaction.previous_tx_hash)

        if previous_transaction == None:
            return False

        return verify_signature(previous_transaction.recipient, transaction.signature, transaction.tx_hash)


    def add_transaction(self, transaction: Transaction) -> bool:
        """
        TODO: Dodaj nową transakcję do listy transakcji.
        Przed dodaniem upewnij się, że:
        - poprzednia transakcja nie została wykorzystana
        - podpis transakcji się zgadza
        wykorzystaj do tego dwie metody powyżej.
        Zwróć True jeśli dodanie transakcji przebiegło pomyślnie, False w przeciwnym wypadku.
        """
        if not self.verify_transaction_signature(transaction):
            return False
        
        if self.is_transaction_spent(transaction.previous_tx_hash):
            return False
        
        self.transactions.append(transaction)
        return True
