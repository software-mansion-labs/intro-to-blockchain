from dataclasses import dataclass
from simple_cryptography import PrivateKey, PublicKey, generate_key_pair, asymmetric_decrypt, asymmetric_encrypt


class Alice:
    def __init__(self, bob: "Bob"):
        self.bob = bob

    def encrypt(self, message: str) -> bytes:
        """
        TODO - zaimplementuj szyfrowanie wiadomości
        Przydadzą ci się funkcje/metody
            - self.bob.get_public_key()
            - bytes(string, 'utf-8')
            - asymmetric_encrypt
        """
        k = self.bob.get_public_key()
        return asymmetric_encrypt(k, bytes(message, 'utf-8'))


class Bob:
    def __init__(self):
        """
        TODO - wygeneruj parę klucz publiczny, prywatny za pomocą metody generate_key_pair z simple_cryptography
        """
        (pub, priv) = generate_key_pair()
        self._private_key: PrivateKey = priv
        self._public_key: PublicKey = pub

    def get_public_key(self):
        return self._public_key

    def decrypt(self, encrypted_message: bytes) -> str:
        """
        TODO - zaimplementuj deszyfrowanie wiadomości
        Przydadzą ci się funkcje/metody
            - self._private_key
            - asymmetric_decrypt
            - string.decode("utf-8")
        """

        return asymmetric_decrypt(self._private_key, encrypted_message).decode("utf-8")