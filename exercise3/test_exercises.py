import pytest

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from exercise3.node import Node, validate_chain, DIFFICULTY
from simple_cryptography import generate_key_pair, sign

(pub1, priv1) = generate_key_pair()
(pub2, priv2) = generate_key_pair()


def test_add_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    init_tx.signature = sign(priv1, init_tx.tx_hash)

    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv1, new_tx.tx_hash)
    node.add_transaction(new_tx)

    assert node.blockchain.length() == 2


def test_throws_on_wrong_transaction():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    init_tx.signature = sign(priv1, init_tx.tx_hash)

    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv2, new_tx.tx_hash)

    with pytest.raises(Exception):
        node.add_transaction(new_tx)


def test_validate_chain():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    init_tx.signature = sign(priv1, init_tx.tx_hash)

    node = Node(pub1, init_tx)

    new_tx = Transaction(recipient=pub2, previous_tx_hash=init_tx.tx_hash)
    new_tx.signature = sign(priv1, new_tx.tx_hash)
    node.add_transaction(new_tx)

    assert validate_chain(node.blockchain)


def test_throws_on_wrong_chain():
    chain = Blockchain([Block(b'\x00', 0, 0, []), Block(b'\x00', 0, 0, [])])

    assert not validate_chain(chain)


def test_find_nonce():
    init_tx = Transaction(recipient=pub1, previous_tx_hash=b'\x00')
    init_tx.signature = sign(priv1, init_tx.tx_hash)

    node = Node(pub1, init_tx)

    block = Block(node.blockchain.get_latest_block().hash, 0, 0, [])
    block = node.find_nonce(block)

    assert int.from_bytes(block.hash, 'big') < DIFFICULTY

