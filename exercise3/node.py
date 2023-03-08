from time import time
from typing import Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature

DIFFICULTY = 1e75


class Node:
    blockchain: Blockchain
    owner: PublicKey

    def __init__(self, owner_public_key: PublicKey, initial_transaction: Transaction):
        self.owner = owner_public_key
        self.blockchain = Blockchain([Block(b'\x00', 0, 0, [initial_transaction])])

    def add_transaction(self, transaction: Transaction):
        """
        Tutaj przychodzi transakcja od użytkownika.
        Tworzona jest transakcja z nowym coinem i z obu powstaje blok.
        Następuje proces kopania i po wykopaniu blok dodawany jest do łańcucha.
        """
        if not self.validate_transaction(transaction):
            raise Exception("Transaction can't be added. Verification failed.")

        new_coin_transaction = Transaction(recipient=self.owner, previous_tx_hash=b'\x00')
        new_block = Block(
            prev_block_hash=self.blockchain.get_latest_block().hash,
            timestamp=int(time()),
            nonce=0,
            transactions=[transaction, new_coin_transaction]
        )

        new_block = self.find_nonce(new_block)
        self.blockchain.blocks.append(new_block)

    def find_nonce(self, block: Block) -> Optional[Block]:
        while int.from_bytes(block.hash, 'big') > DIFFICULTY:
            block.nonce += 1
        return block

    def validate_transaction(self, transaction: Transaction) -> bool:
        if transaction.signature is None:
            return False

        prev_transaction = self.blockchain.get_transaction(transaction.previous_tx_hash)
        if prev_transaction is None:
            return False

        return verify_signature(prev_transaction.recipient, transaction.signature, transaction.tx_hash)

    def get_state(self) -> Blockchain:
        return self.blockchain


def validate_chain(chain: Blockchain) -> bool:
    for index, block in enumerate(chain.blocks[1:]):
        if block.prev_block_hash != chain.blocks[index].hash:
            return False

        if int.from_bytes(block.hash, 'big') > 1e75:
            return False

    return True
