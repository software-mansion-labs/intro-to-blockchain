
from simple_cryptography import PublicKey, sign, verify_signature, generate_key_pair, hash


UMOWA = """
Zgadzam się na wszystko
1. aaaaaaa
2. bbbbbb
3. ccccccc
4. dddddddd
"""


class Alice:

    def __init__(self):
        """
        TODO - wygeneruj parę klucz publiczny, prywatny za pomocą metody generate_key_pair z simple_cryptography
        """
        (pub, priv) = generate_key_pair()
        self._private_key = priv
        self._public_key = pub

    def sign(self) -> bytes:
        """
        TODO - zaimplementuj metodę która podpisuje publiczną umowę - `UMOWA`
        Przydadzą ci się funkcje/metody
            - bytes(string, 'utf-8')
            - hash
            - sign
        """
        return sign(self._private_key, hash(bytes(UMOWA, 'utf-8')))
    
    def get_public_key(self) -> PublicKey:
        return self._public_key

class Bob:

    def __init__(self, alice: Alice): 
        self.alice = alice

    def validate_signature(self, signature) -> bool:
        """
        TODO - zaimplementuj metodę która weryfikuje czy to Alice podpisała umowę
        Przydadzą ci się funkcje/metody
            - self.alice.get_public_key()
            - bytes(string, 'utf-8')
            - hash
            - verify_signature
        """
        return verify_signature(self.alice.get_public_key(), signature, hash(bytes(UMOWA, 'utf-8')))