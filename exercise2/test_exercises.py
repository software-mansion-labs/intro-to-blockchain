from simple_cryptography import generate_key_pair, sign, verify_signature

from exercise2.transaction_registry import (
    Transaction,
    SignedTransaction,
    TransactionRegistry,
)
from exercise2.wallet import Wallet

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()
(pub3, priv3) = generate_key_pair()

initial_transactions = [
    Transaction(pub1, b"0x00"),
    Transaction(pub1, b"0x01"),
    Transaction(pub1, b"0x02"),
    Transaction(pub2, b"0x00"),
    Transaction(pub2, b"0x01"),
    Transaction(pub2, b"0x02"),
    Transaction(pub3, b"0x00"),
    Transaction(pub3, b"0x01"),
    Transaction(pub3, b"0x02"),
]


def test_get_transaction():
    reg = TransactionRegistry(initial_transactions)

    assert (
        reg.get_transaction(initial_transactions[2].tx_hash) == initial_transactions[2]
    )

    assert (
        reg.get_transaction(b"12345") is None
    ), "get_transaction should return None for non-existent tx hash"


def test_is_transaction_available():
    new_transaction = Transaction(pub2, initial_transactions[0].tx_hash)

    signature = sign(priv1, new_transaction.tx_hash)

    new_transaction = SignedTransaction.from_transaction(new_transaction, signature)

    reg = TransactionRegistry(initial_transactions + [new_transaction])

    assert not reg.is_transaction_available(
        b"12345"
    ), "Transaction does not exist, should return False"

    assert reg.is_transaction_available(new_transaction.tx_hash)

    assert reg.is_transaction_available(initial_transactions[1].tx_hash)
    assert reg.is_transaction_available(initial_transactions[2].tx_hash)

    assert not reg.is_transaction_available(initial_transactions[0].tx_hash)


def test_verify_transaction_signature():
    reg = TransactionRegistry(initial_transactions)

    new_transaction = Transaction(pub2, initial_transactions[0].tx_hash)
    signature = sign(priv1, new_transaction.tx_hash)
    new_transaction = SignedTransaction.from_transaction(new_transaction, signature)

    assert reg.verify_transaction_signature(new_transaction)

    incorrect_tx0 = Transaction(pub2, b"12345")
    signature = sign(priv1, incorrect_tx0.tx_hash)
    incorrect_tx0 = SignedTransaction.from_transaction(incorrect_tx0, signature)

    assert not reg.verify_transaction_signature(incorrect_tx0)

    incorrect_tx1 = Transaction(pub2, initial_transactions[0].tx_hash)
    signature = sign(priv3, incorrect_tx1.tx_hash)
    incorrect_tx1 = SignedTransaction.from_transaction(incorrect_tx0, signature)

    assert not reg.verify_transaction_signature(incorrect_tx1)


def test_add_transaction():
    reg = TransactionRegistry(initial_transactions)

    new_tx1 = Transaction(pub2, initial_transactions[0].tx_hash)
    new_tx1 = SignedTransaction.from_transaction(new_tx1, sign(priv1, new_tx1.tx_hash))

    new_tx2 = Transaction(pub3, new_tx1.tx_hash)
    new_tx2 = SignedTransaction.from_transaction(new_tx2, sign(priv2, new_tx2.tx_hash))

    assert reg.add_transaction(new_tx1)
    assert not reg.add_transaction(new_tx1)

    assert reg.add_transaction(new_tx2)
    assert not reg.add_transaction(new_tx2)

    new_tx3 = SignedTransaction(pub1, new_tx2.tx_hash, b"12345")

    assert not reg.add_transaction(new_tx3)

    new_tx4 = Transaction(pub1, b"12345")
    new_tx4 = SignedTransaction.from_transaction(new_tx4, sign(priv3, new_tx4.tx_hash))

    assert not reg.add_transaction(new_tx4)


def test_get_available_transactions():
    reg = TransactionRegistry(initial_transactions)

    wallet = Wallet((pub1, priv1))

    txs = wallet.get_available_transactions(reg)

    assert initial_transactions[0] in txs
    assert initial_transactions[1] in txs
    assert initial_transactions[2] in txs

    tx = Transaction(pub2, initial_transactions[0].tx_hash)
    tx = SignedTransaction.from_transaction(tx, sign(priv1, tx.tx_hash))

    assert reg.add_transaction(tx)

    txs = wallet.get_available_transactions(reg)

    assert not initial_transactions[0] in txs


def test_get_balance():
    reg = TransactionRegistry(initial_transactions)

    wallet = Wallet((pub1, priv1))

    assert wallet.get_balance(reg) == 3

    tx = Transaction(pub2, initial_transactions[0].tx_hash)
    tx = SignedTransaction.from_transaction(tx, sign(priv1, tx.tx_hash))

    assert reg.add_transaction(tx)
    assert wallet.get_balance(reg) == 2


def test_transfer():
    reg = TransactionRegistry(initial_transactions)

    wallet1 = Wallet((pub1, priv1))
    wallet2 = Wallet((pub2, priv2))

    assert wallet1.transfer(reg, wallet2.public_key)

    assert wallet1.get_balance(reg) == 2
    assert wallet2.get_balance(reg) == 4

    assert wallet1.transfer(reg, wallet2.public_key)
    assert wallet1.transfer(reg, wallet2.public_key)

    assert wallet1.get_balance(reg) == 0
    assert wallet2.get_balance(reg) == 6

    assert not wallet1.transfer(reg, wallet2.public_key)


def test_sign_transaction():
    wallet1 = Wallet((pub1, priv1))
    wallet2 = Wallet((pub2, priv2))

    tx = Transaction(wallet2.public_key, initial_transactions[0].tx_hash)
    signed_tx = wallet1.sign_transaction(tx)

    assert verify_signature(wallet1.public_key, signed_tx.signature, signed_tx.tx_hash)
