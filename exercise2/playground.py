from exercise2.wallet import Wallet
from exercise2.transaction_registry import Transaction, TransactionRegistry
from simple_cryptography import generate_key_pair

alice = Wallet(generate_key_pair())
bob = Wallet(generate_key_pair())

# Początkowe transakcje, bez podpisów.
# Jest to nasz sposób na wprowadzenie nowych coinów do rejestru.
# Podajemy różne wartości dla previous_tx_hash, żeby hashe transakcji nie były takie same.
# Bitcoin rozwiązuje to inaczej, ale o tym później...
initial_transactions = [
    Transaction(alice.public_key, b"\x00"),
    Transaction(alice.public_key, b"\x01"),
    Transaction(alice.public_key, b"\x02"),
    Transaction(bob.public_key, b"\x00"),
    Transaction(bob.public_key, b"\x01"),
]

registry = TransactionRegistry(initial_transactions)


def print_balances():
    print(f"Alice's balance: {alice.get_balance(registry)}")
    print(f"Bob's balance: {bob.get_balance(registry)}")

print_balances()

alice.transfer(registry, bob.public_key)

print_balances()

alice.transfer(registry, bob.public_key)

print_balances()

bob.transfer(registry, alice.public_key)

print_balances()
