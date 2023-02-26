
from simple_cryptography import PublicKey, sign, verify_signature, generate_key_pair


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
        self._private_key = "TODO"
        self._public_key = "TODO"

    def sign(self) -> bytes:
        """
        TODO - zaimplementuj metodę która podpisuje publiczną umowę - `UMOWA`
        Przydadzą ci się funkcje/metody
            - bytes(string, 'utf-8')
            - hash
            - sign
        """
        raise NotImplementedError()

    
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
        raise NotImplementedError()
