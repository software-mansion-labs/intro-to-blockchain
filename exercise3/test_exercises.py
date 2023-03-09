import pytest

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from exercise3.node import Node, validate_chain, DIFFICULTY
from simple_cryptography import generate_key_pair, sign

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()


# Blockchain

def test_get_latest_block():
    block = Block(b'\x00', 0, 0, [])
    chain = Blockchain([block])

    assert chain.get_latest_block() == block


def test_length():
    block = Block(b'\x00', 0, 0, [])
    chain = Blockchain([block]*24)

    assert chain.length() == 24


def test_get_transaction():
    transaction = Transaction(pub1, b'\x00')
    block = Block(b'\x00', 0, 0, [transaction])
    chain = Blockchain([block])

    assert chain.get_transaction(transaction.tx_hash) == transaction


def test_get_nonexistent_transaction():
    transaction = Transaction(pub1, b'\x00')
    block = Block(b'\x00', 0, 0, [transaction])
    chain = Blockchain([block])

    assert chain.get_transaction(tx_hash=b'\x00') is None


# Node

def test__node_init():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    assert node.owner == pub1
    assert node.blockchain.length() == 1
    assert init_tx in node.blockchain.get_latest_block().transactions


def test_add_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv1, new_tx.tx_hash)
    node.add_transaction(new_tx)

    assert node.blockchain.length() == 2
    assert new_tx in node.blockchain.get_latest_block().transactions


def test_add_transaction_throws_on_wrong_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    # Użytkownik z kluczem publicznym `pub2` próbuje przekazać sobie coin'a należącego do pub1
    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv2, new_tx.tx_hash)

    with pytest.raises(Exception):
        node.add_transaction(new_tx)


def test_validate_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv1, new_tx.tx_hash)

    assert node.validate_transaction(new_tx)


def test_validate_transaction_throws_on_wrong_tx():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    wrong_user = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    wrong_user.signature = sign(priv2, wrong_user.tx_hash)

    coin_does_not_exist = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    coin_does_not_exist.signature = sign(priv2, coin_does_not_exist.tx_hash)

    assert not node.validate_transaction(wrong_user)
    assert not node.validate_transaction(coin_does_not_exist)


def test_validate_chain():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv1, new_tx.tx_hash)
    node.add_transaction(new_tx)

    assert validate_chain(node.blockchain)


def test_validate_chain_throws_on_wrong_chain():
    chain = Blockchain([Block(b'\x00', 0, 0, []), Block(b'\x00', 0, 0, [])])

    assert not validate_chain(chain)


def test_find_nonce():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    node = Node(pub1, init_tx)

    block = Block(node.blockchain.get_latest_block().hash, 0, 0, [])
    block = node.find_nonce(block)

    assert int.from_bytes(block.hash, 'big') < DIFFICULTY
