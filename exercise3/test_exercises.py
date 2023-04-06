from time import time

import pytest

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from exercise3.node import Node, validate_chain, DIFFICULTY, MAX_256_INT
from simple_cryptography import generate_key_pair, sign

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()


# Blockchain


def test_get_latest_block():
    block = Block(b"\x00", 0, 0, [])
    chain = Blockchain([block])

    assert chain.get_latest_block() == block


def test_length():
    block = Block(b"\x00", 0, 0, [])
    chain = Blockchain([block] * 24)

    assert chain.length() == 24


def test_get_transaction():
    transaction = Transaction(pub1, b"\x00")
    block = Block(b"\x00", 0, 0, [transaction])
    chain = Blockchain([block])

    assert chain.get_transaction_by(tx_hash=transaction.hash) == transaction


def test_get_nonexistent_transaction():
    transaction = Transaction(pub1, b"\x00")
    block = Block(b"\x00", 0, 0, [transaction])
    chain = Blockchain([block])

    assert chain.get_transaction_by(tx_hash=b"\x00") is None


def test_get_transaction_by_raises_at_two_arguments():
    transaction = Transaction(pub1, b"\x00")
    block = Block(b"\x00", 0, 0, [transaction])
    chain = Blockchain([block])

    with pytest.raises(Exception):
        chain.get_transaction_by(b"\x00", b"\x00")


# Node


def test__node_init():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    assert node.owner == pub1
    assert node.blockchain.length() == 1
    assert init_tx in node.blockchain.get_latest_block().transactions


def test_add_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)
    node.add_transaction(new_tx)

    assert node.blockchain.length() == 2
    assert new_tx in node.blockchain.get_latest_block().transactions


def test_add_transaction_throws_on_wrong_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    # Użytkownik z kluczem publicznym `pub2` próbuje przekazać sobie coin'a należącego do pub1
    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv2)

    with pytest.raises(Exception):
        node.add_transaction(new_tx)


def test_add_transaction_throws_on_spending_spent_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)
    node.add_transaction(new_tx)

    with pytest.raises(Exception):
        # Próba wydania wcześniej wydanego coin'a
        node.add_transaction(new_tx)


def test_validate_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)

    assert node.validate_transaction(new_tx)


def test_validate_transaction_throws_on_wrong_tx():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    # Użytkownik, do którego nie należy coin, próbuje go wydać
    wrong_user_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    wrong_user_tx.sign(priv2)

    # Coin, który próbujemy wydać nie istnieje
    coin_does_not_exist_tx = Transaction(recipient=pub2, previous_tx_hash=b"\x03")
    coin_does_not_exist_tx.sign(priv1)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)
    node.add_transaction(new_tx)

    assert not node.validate_transaction(wrong_user_tx)
    assert not node.validate_transaction(coin_does_not_exist_tx)
    # Próba wydania wcześniej wydanego coin'a
    assert not node.validate_transaction(new_tx)


def test_validate_valid_chain():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)
    node.add_transaction(new_tx)

    assert validate_chain(node.blockchain)


def test_validate_chain_with_wrong_block():
    chain = Blockchain([Block(b"\x00", 0, 0, []), Block(b"\x00", 0, 0, [])])

    assert not validate_chain(chain)


def test_validate_chain_with_wrong_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv2)

    new_coin_transaction = Transaction(recipient=node.owner, previous_tx_hash=b"\x00")
    new_block = Block(
        prev_block_hash=node.blockchain.get_latest_block().hash,
        timestamp=int(time()),
        nonce=0,
        transactions=[new_tx, new_coin_transaction],
    )

    new_block = node.find_nonce(new_block)
    node.blockchain.blocks.append(new_block)

    assert not validate_chain(node.blockchain)


def test_validate_chain_with_wrong_new_coin_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_coin_transaction = Transaction(recipient=node.owner, previous_tx_hash=b"\x00")
    new_coin_transaction2 = Transaction(recipient=node.owner, previous_tx_hash=b"\x00")
    new_block = Block(
        prev_block_hash=node.blockchain.get_latest_block().hash,
        timestamp=int(time()),
        nonce=0,
        transactions=[new_coin_transaction, new_coin_transaction2],
    )

    new_block = node.find_nonce(new_block)
    node.blockchain.blocks.append(new_block)

    assert not validate_chain(node.blockchain)


def test_find_nonce():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    block = Block(node.blockchain.get_latest_block().hash, 0, 0, [])
    block = node.find_nonce(block)

    assert int.from_bytes(block.hash, "big") < MAX_256_INT >> DIFFICULTY


def test_node_owner_gets_coin():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b"\x00")
    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.hash)
    new_tx.sign(priv1)
    node.add_transaction(new_tx)

    owners = [tx.recipient for tx in node.blockchain.get_latest_block().transactions]
    assert pub1 in owners
