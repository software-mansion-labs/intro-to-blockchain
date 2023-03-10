from exercise1.hash_1 import Transaction
from exercise1.public_key_2 import Alice, Bob
from exercise1 import signature_3
from simple_cryptography import generate_key_pair, sign

def test_hash():
    assert Transaction(1, 2, "xDDDDDD").hash() == b'\xf5\xa2\x81\x19\xfc\xd3eNI\tN\x8b)\xd2\xb9oZ\x11\xe7:\xc7\xec\x04\xca\xfb\xc8\x0fF\x0f1\xa9\xdf'

secrect_message = """
To jest tajna wiadomość która nigdy nie powinna zostać odczytana
"""

def test_encryption():
    bob = Bob()
    alice = Alice(bob)
    encrypted = alice.encrypt(secrect_message)
    assert encrypted != secrect_message
    decrypted = bob.decrypt(encrypted)
    assert secrect_message == decrypted
    

def test_signature():
    alice = signature_3.Alice()
    bob = signature_3.Bob(alice)
    signature = alice.sign()
    assert bob.validate_signature(signature)


def test_malicious_alice():
    alice = signature_3.Alice()
    bob = signature_3.Bob(alice)
    (_, priv) = generate_key_pair()
    somebody_else_signed = sign(priv, bytes(signature_3.UMOWA, "utf-8"))
    assert not bob.validate_signature(somebody_else_signed)
