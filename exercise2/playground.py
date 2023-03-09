from exercise2.wallet import Wallet
from exercise2.transaction_registry import Transaction, TransactionRegistry
from simple_cryptography import generate_key_pair

alice = Wallet(generate_key_pair())
bob = Wallet(generate_key_pair())

initial_transactions = [
    Transaction(alice.public_key, b'0x00'),
    Transaction(alice.public_key, b'0x01'),
    Transaction(alice.public_key, b'0x02'),
    Transaction(bob.public_key, b'0x00'),
    Transaction(bob.public_key, b'0x01'),
]

registry = TransactionRegistry(initial_transactions)

def print_balances():
    print(f"Alice's balance: {alice.get_balance(registry)}")
    print(f"Bob's balance: {bob.get_balance(registry)}")

alice.transfer(registry, bob.public_key)

print_balances()

alice.transfer(registry, bob.public_key)

print_balances()

bob.transfer(registry, alice.public_key)

print_balances()
