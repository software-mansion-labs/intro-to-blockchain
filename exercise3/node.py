from time import time
from typing import List, Optional, Tuple

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature

DIFFICULTY = 1e75


class Node:
    blockchain: Blockchain
    other_nodes: List["Node"]
    owner: PublicKey

    def __init__(self, owner_public_key: PublicKey, initial_transaction: Transaction):
        self.other_nodes = []
        self.owner = owner_public_key
        self.blockchain = Blockchain([Block(b'\x00', 0, 0, [initial_transaction])])

    def add_transaction(self, transaction: Transaction, from_node: bool = False):
        """
        Tutaj przychodzi transakcja od użytkownika lub taka przekazana przez node.
        Tworzona jest transakcja z nowym coinem i z obu powstaje blok.
        Następuje proces kopania i po wykopaniu łańcuch jest przekazywany do innych node'ów.
        """
        if not self.validate_transaction(transaction):
            raise Exception("Transaction can't be added. Verification failed.")

        if not from_node:
            self.pass_transaction_to_other_nodes(transaction)

        new_coin_transaction = Transaction(recipient=self.owner, previous_tx_hash=b'\x00')
        new_block = Block(
            prev_block_hash=self.blockchain.get_latest_block().hash,
            timestamp=int(time()),
            nonce=0,
            transactions=[transaction, new_coin_transaction]
        )

        new_block = self.find_nonce(new_block)
        if new_block is None:
            return
        self.blockchain.blocks.append(new_block)

        self.pass_chain_to_other_nodes()

    def find_nonce(self, block: Block) -> Optional[Block]:
        while int.from_bytes(block.hash, 'big') > DIFFICULTY:
            if self.blockchain.get_latest_block().hash != block.prev_block_hash:
                return None
            block.nonce += 1
        return block

    def pass_transaction_to_other_nodes(self, transaction: Transaction):
        for node in self.other_nodes:
            node.add_transaction(transaction, from_node=True)

    def pass_chain_to_other_nodes(self):
        for node in self.other_nodes:
            node.validate_chain(self.blockchain)

    def validate_transaction(self, transaction: Transaction) -> bool:
        if transaction.signature is None:
            return False

        prev_transaction = self.blockchain.get_transaction(transaction.previous_tx_hash)
        if prev_transaction is None:
            return False

        return verify_signature(prev_transaction.recipient, transaction.signature, transaction.tx_hash)

    def get_state(self) -> Tuple[Blockchain, List["Node"]]:
        return self.blockchain, self.other_nodes

    def register_new_node(self, node: "Node"):
        self.other_nodes.append(node)

    def join_network(self, parent_node: "Node"):
        chain, other_nodes = parent_node.get_state()

        self.blockchain = chain
        self.other_nodes = other_nodes + [parent_node]

        for node in self.other_nodes:
            node.register_new_node(self)


def validate_chain(chain: Blockchain) -> bool:
    for index, block in enumerate(chain.blocks[1:]):
        if block.prev_block_hash != chain.blocks[index].hash:
            return False

        if int.from_bytes(block.hash, 'big') > 1e75:
            return False

    return True


if __name__ == '__main__':
    node = Node(123)

    node.add_transaction(Transaction(1, 2, 'abc'))

    print(node.get_state())
