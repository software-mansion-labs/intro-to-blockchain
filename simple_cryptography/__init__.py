"""
This module is for educational purposes only
Do not use it as a cryptography library
"""
from typing import Tuple
from attr import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def hash(value: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(value)
    return digest.finalize()

@dataclass
class PrivateKey:
    value: rsa.RSAPrivateKey

@dataclass
class PublicKey:
    value: rsa.RSAPublicKey

def generate_key_pair() -> Tuple[PublicKey, PrivateKey]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return (PublicKey(public_key), PrivateKey(private_key))

def asymmetric_encrypt(public_key: PublicKey, message: bytes) -> bytes:
    return public_key.value.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def asymmetric_decrypt(private_key: PrivateKey, encrypted_message: bytes) -> bytes:
    plaintext = private_key.value.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext
