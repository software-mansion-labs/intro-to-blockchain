from simple_cryptography import generate_key_pair, sign

from exercise2.transaction_registry import Transaction, TransactionRegistry

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()
(pub3, priv3) = generate_key_pair()

initial_transactions = [
  Transaction(pub1, b'0', b''),
  Transaction(pub1, b'1', b''),
  Transaction(pub1, b'2', b''),
  Transaction(pub2, b'0', b''),
  Transaction(pub2, b'1', b''),
  Transaction(pub2, b'2', b''),
  Transaction(pub3, b'0', b''),
  Transaction(pub3, b'1', b''),
  Transaction(pub3, b'2', b''),
]

def test_get_transaction():
    reg = TransactionRegistry(initial_transactions)

    assert reg.get_transaction(initial_transactions[2].tx_hash) == initial_transactions[2]

    assert reg.get_transaction(b'12345') == None

def test_is_transaction_spent():
    new_transaction = Transaction(pub2, initial_transactions[0].tx_hash, None)
    
    new_transaction.signature = sign(priv1, new_transaction.tx_hash)

    reg = TransactionRegistry(initial_transactions + [new_transaction])

    assert not reg.is_transaction_spent(new_transaction.tx_hash)

    assert not reg.is_transaction_spent(initial_transactions[1].tx_hash)
    assert not reg.is_transaction_spent(initial_transactions[2].tx_hash)

    assert reg.is_transaction_spent(initial_transactions[0].tx_hash)

def test_add_transaction():
    reg = TransactionRegistry(initial_transactions)

    new_tx1 = Transaction(pub2, initial_transactions[0].tx_hash, None)
    new_tx1.signature = sign(priv1, new_tx1.tx_hash)

    new_tx2 = Transaction(pub3, new_tx1.tx_hash, None)
    new_tx2.signature = sign(priv2, new_tx2.tx_hash)

    assert reg.add_transaction(new_tx1)
    assert reg.add_transaction(new_tx2)
