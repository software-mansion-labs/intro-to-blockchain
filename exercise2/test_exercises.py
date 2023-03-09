from simple_cryptography import generate_key_pair, sign, verify_signature

from exercise2.transaction_registry import Transaction, SignedTransaction, TransactionRegistry
from exercise2.wallet import Wallet

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()
(pub3, priv3) = generate_key_pair()

initial_transactions = [
  Transaction(pub1, b'0x00'),
  Transaction(pub1, b'0x01'),
  Transaction(pub1, b'0x02'),
  Transaction(pub2, b'0x00'),
  Transaction(pub2, b'0x01'),
  Transaction(pub2, b'0x02'),
  Transaction(pub3, b'0x00'),
  Transaction(pub3, b'0x01'),
  Transaction(pub3, b'0x02'),
]

def test_get_transaction():
    reg = TransactionRegistry(initial_transactions)

    assert reg.get_transaction(initial_transactions[2].tx_hash) == initial_transactions[2]

    assert reg.get_transaction(b'12345') == None

def test_is_transaction_spent():
    print(len(initial_transactions))
    new_transaction = Transaction(pub2, initial_transactions[0].tx_hash)
    
    signature = sign(priv1, new_transaction.tx_hash)

    new_transaction = SignedTransaction(new_transaction, signature)

    reg = TransactionRegistry(initial_transactions + [new_transaction])

    assert not reg.is_transaction_spent(new_transaction.tx_hash)

    assert not reg.is_transaction_spent(initial_transactions[1].tx_hash)
    assert not reg.is_transaction_spent(initial_transactions[2].tx_hash)

    assert reg.is_transaction_spent(initial_transactions[0].tx_hash)

def test_add_transaction():
    reg = TransactionRegistry(initial_transactions)

    new_tx1 = Transaction(pub2, initial_transactions[0].tx_hash)
    new_tx1 = SignedTransaction(new_tx1, sign(priv1, new_tx1.tx_hash))

    new_tx2 = Transaction(pub3, new_tx1.tx_hash)
    new_tx2 = SignedTransaction(new_tx2, sign(priv2, new_tx2.tx_hash))

    assert reg.add_transaction(new_tx1)
    assert reg.add_transaction(new_tx2)

def test_get_unspent_transactions():
    reg = TransactionRegistry(initial_transactions)

    wallet = Wallet((pub1, priv1))

    txs = wallet.get_unspent_transactions(reg)

    assert initial_transactions[0] in txs
    assert initial_transactions[1] in txs
    assert initial_transactions[2] in txs

def test_get_balance():
    reg = TransactionRegistry(initial_transactions)

    wallet = Wallet((pub1, priv1))

    assert wallet.get_balance(reg) == 3

def test_transfer():
    reg = TransactionRegistry(initial_transactions)

    wallet1 = Wallet((pub1, priv1))
    wallet2 = Wallet((pub2, priv2))

    assert wallet1.transfer(reg, wallet2.public_key)

    assert wallet1.get_balance(reg) == 2
    assert wallet2.get_balance(reg) == 4

def test_sign_transaction():
    reg = TransactionRegistry(initial_transactions)

    wallet1 = Wallet((pub1, priv1))
    wallet2 = Wallet((pub2, priv2))

    tx = Transaction(wallet2.public_key, initial_transactions[0].tx_hash)
    signed_tx = wallet1.sign_transaction(tx)

    assert verify_signature(wallet1.public_key, signed_tx.signature, signed_tx.tx_hash)
