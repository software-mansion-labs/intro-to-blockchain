from exercise1.hash_1 import Transaction
from exercise1.public_key_2 import Alice, Bob

def test_hash():
    assert Transaction(1, 2, "xDDDDDD").hash() == b"'sP[B9\x99\xec\xc1`\xf7\xcb?\xe9\xf6R\xf8\xe3v\x1f4\t\xecX%\xec\xc0\x0f{\xad\x0fN"

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
    