import os
import hashlib

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from cryptography.hazmat.primitives import padding


def derive_key(password: str) -> bytes:
    """
    Convert password into 32-byte AES-256 key
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).digest()


def encrypt_message(message: str, password: str) -> bytes:
    """
    Encrypt text using AES-256 CBC
    """

    key = derive_key(password)

    # Random 16-byte IV
    iv = os.urandom(16)

    # PKCS7 padding
    padder = padding.PKCS7(128).padder()

    padded_data = (
        padder.update(message.encode("utf-8"))
        + padder.finalize()
    )

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    ciphertext = (
        encryptor.update(padded_data)
        + encryptor.finalize()
    )

    # Store IV + ciphertext together
    return iv + ciphertext


def decrypt_message(
    encrypted_bytes: bytes,
    password: str
) -> str:

    key = derive_key(password)

    # First 16 bytes = IV
    iv = encrypted_bytes[:16]

    ciphertext = encrypted_bytes[16:]

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_data = (
        decryptor.update(ciphertext)
        + decryptor.finalize()
    )

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()

    data = (
        unpadder.update(padded_data)
        + unpadder.finalize()
    )

    return data.decode("utf-8")


def bytes_to_bits(data: bytes) -> str:
    """
    Convert bytes into binary string
    """

    return ''.join(
        format(byte, '08b')
        for byte in data
    )


def bits_to_bytes(bits: str) -> bytes:
    """
    Convert binary string back into bytes
    """

    byte_array = []

    for i in range(0, len(bits), 8):

        chunk = bits[i:i+8]

        if len(chunk) == 8:

            byte_array.append(
                int(chunk, 2)
            )

    return bytes(byte_array)


if __name__ == "__main__":

    password = "MySecretPassword123"

    message = "This is a secret message for FAANG!"

    encrypted = encrypt_message(
        message,
        password
    )

    print("Encrypted bytes:")
    print(encrypted[:20])

    decrypted = decrypt_message(
        encrypted,
        password
    )

    print("\nDecrypted:")
    print(decrypted)

    assert message == decrypted

    print("\n✅ AES-256 working correctly")