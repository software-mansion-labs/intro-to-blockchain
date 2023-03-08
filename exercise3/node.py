import asyncio
import pickle
import random
from time import time, sleep
from typing import List, Optional

import requests as requests
from aiohttp import ClientSession
from flask import request

from exercise1.hash_1 import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain

from exercise3.server import Server


class Node(Server):
    blockchain: Blockchain
    other_nodes_addresses: List[str]

    def __init__(self, node_name: str):
        super().__init__(node_name)

        self.blockchain = Blockchain([Block(b'\x00', 0, 0, [])])
        self.other_nodes_addresses = []

        self.add_endpoint(path='/transaction/add', type='POST', method_name='add_transaction', method=self.add_transaction)
        self.add_endpoint(path='/nodes/register', type='POST', method_name='register_node', method=self.register_new_node)
        self.add_endpoint(path='/state', type='GET', method_name='get_state', method=self.get_state)
        self.add_endpoint(path='/join-network', type='POST', method_name='join_network', method=self.join_network)
        self.add_endpoint(path='/validate', type='POST', method_name='validate_chain', method=self.validate_chain)

    def add_transaction(self):
        """
        Tutaj przychodzi transakcja od użytkownika lub taka przekazana przez node.
        Tworzona jest transakcja z nowym coinem i z obu powstaje blok.
        Następuje proces kopania i po wykopaniu łańcuch jest przekazywany do innych node'ów.
        """
        args = pickle.loads(request.data)
        transaction = args['transaction']
        if not args.get('from_node', False):
            self.pass_transaction_to_other_nodes(transaction)

        add_coin_transaction = Transaction(0, 2, "")
        new_block = Block(
            prev_block_hash=self.blockchain.get_latest_block().hash,
            timestamp=int(time()),
            nonce=0,
            transactions=[transaction, add_coin_transaction]
        )

        new_block = self.find_nonce(new_block)
        if new_block is None:
            return '', 200
        self.blockchain.blocks.append(new_block)

        self.pass_chain_to_other_nodes()

        return '', 200

    def find_nonce(self, block: Block) -> Optional[Block]:
        # TODO: Choose a proper number
        while int.from_bytes(block.hash, 'big') > 1e75:
            sleep(random.randint(1, 2) / 10)
            if self.blockchain.get_latest_block().hash != block.prev_block_hash:
                return None
            block.nonce += 1
        return block

    def pass_transaction_to_other_nodes(self, transaction: Transaction):
        for node in self.other_nodes_addresses:
            requests.post(
                url=node + '/transaction/add',
                data=pickle.dumps({'transaction': transaction, 'from_node': True})
            )

    def pass_chain_to_other_nodes(self):
        for node in self.other_nodes_addresses:
            requests.post(
                url=node + '/validate', data=pickle.dumps(self.blockchain)
            )
        return '', 200

    def validate_chain(self):
        chain: Blockchain = pickle.loads(request.data)
        if chain.length() > self.blockchain.length():
            self.blockchain = chain
        elif chain.length() == self.blockchain.length() and chain.get_latest_block().timestamp < self.blockchain.get_latest_block().timestamp:
            self.blockchain = chain

        return '', 200

    def get_state(self):
        return pickle.dumps({
            "nodes": self.other_nodes_addresses,
            "blockchain": self.blockchain
        })

    def register_new_node(self):
        new_node_address = request.form.get("address")
        self.other_nodes_addresses.append(new_node_address)

        return '', 200

    def join_network(self):
        parent_address = request.form.get('parent_address')
        state = pickle.loads(
            requests.get(
                url=parent_address + '/state',
            ).content
        )

        self.blockchain = state["blockchain"]
        self.other_nodes_addresses = state["nodes"] + [parent_address]

        for node in self.other_nodes_addresses:
            requests.post(
                url=node + '/nodes/register',
                data={"address": 'http://' + request.host}
            )

        return '', 200


async def run_node(port):
    node = Node("")
    node.app.run(port=port, threaded=True)


async def join_network(port):
    async with ClientSession(base_url="http://127.0.0.1:" + str(port)) as session:
        await session.post(
            url='/join-network', data={"parent_address": "http://127.0.0.1:5000"}
        )


if __name__ == '__main__':
    asyncio.run(run_node(5000))  # genesis node
    # asyncio.run(run_node(5001))
    # asyncio.run(run_node(5002))
    # asyncio.run(join_network(5001))
    # asyncio.run(join_network(5002))
