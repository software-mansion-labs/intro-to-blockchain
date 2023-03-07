from simple_cryptography import hash, PublicKey, verify_signature

class Transaction:
    recipient: PublicKey    
    previous_tx_hash: bytes
    tx_hash: bytes
    signature: bytes

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes, signature: bytes = None):
        self.recipient = recipient
        self.previous_tx_hash = previous_tx_hash
        self.signature = signature
        self.tx_hash = hash(recipient.public_bytes() + previous_tx_hash)

class TransactionRegistry:
    transactions: list[Transaction]

    def __init__(self, initial_transactions: list[Transaction]):
        self.transactions = initial_transactions

    def get_transaction(self, tx_hash: bytes) -> Transaction:
        for tx in self.transactions:
            if tx.tx_hash == tx_hash:
                return tx    
        
        return None

    def is_transaction_spent(self, tx_hash: bytes) -> bool:
        """
        TODO: Sprawdź czy transakcja o podanym hashu została wykorzystana - tj. czy istnieje inna transakcja
        dla której ta transakcja jest wcześniejszą transakcją. (pole previous_tx_hash).

        W przypadku gdy transakcja o hashu tx_hash nie istnieje, zwróć false.
        """

        for tx in self.transactions:
            if tx.previous_tx_hash == tx_hash:
                return True
        
        return False

    def verify_transaction_signature(self, transaction: Transaction) -> bool:
        """
        TODO: Dla podanej transakcji zweryfikuj jej podpis, względem klucza publicznego poprzedniej transakcji.
        Przypomnienie: podpisywany jest hash transakcji.
        """
        previous_transaction = self.get_transaction(transaction.previous_tx_hash)

        return verify_signature(previous_transaction.recipient, transaction.signature, transaction.tx_hash)


    def add_transaction(self, transaction: Transaction) -> bool:
        """
        TODO: Dodaj nową transakcję do listy transakcji.
        Przed dodaniem upewnij się, że:
        - poprzednia transakcja nie została wykorzystana
        - podpis transakcji się zgadza
        wykorzystaj do tego dwie metody powyżej.
        """
        if not self.verify_transaction_signature(transaction):
            return False
        
        if self.is_transaction_spent(transaction.previous_tx_hash):
            return False
        
        self.transactions.append(transaction)
        return True
