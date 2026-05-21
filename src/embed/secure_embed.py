from src.embed.aes_encrypt import (
    encrypt_message,
    decrypt_message,
    bytes_to_bits,
    bits_to_bytes
)

from src.embed.image_utils import (
    get_image_capacity
)

from PIL import Image

import numpy as np
import struct


# ----------------------------------------
# Magic header to identify stego payload
# ----------------------------------------

MAGIC_HEADER = b"STEG"


# ========================================
# SECURE EMBED
# ========================================

def secure_embed(
    image_path: str,
    message: str,
    password: str,
    output_path: str
) -> dict:

    """
    Encrypt message using AES-256
    then embed into image using LSB.
    """

    # ----------------------------------------
    # Validate image format
    # ----------------------------------------

    capacity = get_image_capacity(image_path)

    if not capacity["can_use"]:

        raise ValueError(
            capacity["error"]
        )

    # ----------------------------------------
    # Encrypt message
    # ----------------------------------------

    encrypted_bytes = encrypt_message(
        message,
        password
    )

    # ----------------------------------------
    # Build payload
    #
    # Structure:
    # MAGIC_HEADER (4 bytes)
    # + payload length (4 bytes)
    # + encrypted data
    # ----------------------------------------

    payload = (

        MAGIC_HEADER

        + struct.pack(
            ">I",
            len(encrypted_bytes)
        )

        + encrypted_bytes
    )

    # ----------------------------------------
    # Convert payload to binary string
    # ----------------------------------------

    binary_data = bytes_to_bits(payload)

    # ----------------------------------------
    # Load image
    # ----------------------------------------

    img = Image.open(image_path).convert("RGB")

    pixels = np.array(img)

    flat = pixels.flatten()

    # ----------------------------------------
    # Capacity check
    # ----------------------------------------

    if len(binary_data) > len(flat):

        raise ValueError(
            f"Image too small.\n"
            f"Need {len(binary_data)} bits,\n"
            f"have {len(flat)} bits."
        )

    # ----------------------------------------
    # Embed bits
    # ----------------------------------------

    for i in range(len(binary_data)):

        flat[i] = (

            (flat[i] & 0xFE)

            | int(binary_data[i])
        )

    # ----------------------------------------
    # Reshape and save image
    # ----------------------------------------

    stego_pixels = flat.reshape(
        pixels.shape
    )

    stego_img = Image.fromarray(
        stego_pixels.astype(np.uint8)
    )

    stego_img.save(
        output_path,
        "PNG"
    )

    # ----------------------------------------
    # Return metadata
    # ----------------------------------------

    return {

        "status": "success",

        "message_length": len(message),

        "encrypted_size_bytes":
            len(encrypted_bytes),

        "bits_used":
            len(binary_data),

        "capacity_used_percent":
            round(
                len(binary_data)
                / len(flat)
                * 100,
                2
            ),

        "output_image":
            output_path
    }


# ========================================
# SECURE EXTRACT
# ========================================

def secure_extract(
    image_path: str,
    password: str
) -> str:

    """
    Extract encrypted payload
    then decrypt using AES-256.
    """

    # ----------------------------------------
    # Load image
    # ----------------------------------------

    img = Image.open(image_path).convert("RGB")

    pixels = np.array(img)

    flat = pixels.flatten()

    # ----------------------------------------
    # Extract all LSB bits
    # ----------------------------------------

    bits = ""

    for pixel in flat:

        bits += str(pixel & 1)

    # ----------------------------------------
    # Convert bits back to bytes
    # ----------------------------------------

    extracted_bytes = bits_to_bytes(bits)

    # ----------------------------------------
    # Verify header
    # ----------------------------------------

    if extracted_bytes[:4] != MAGIC_HEADER:

        return (
            "❌ No hidden encrypted "
            "content found."
        )

    # ----------------------------------------
    # Read encrypted payload length
    # ----------------------------------------

    data_length = struct.unpack(
        ">I",
        extracted_bytes[4:8]
    )[0]

    # ----------------------------------------
    # Extract encrypted payload
    # ----------------------------------------

    encrypted_data = extracted_bytes[
        8:8 + data_length
    ]

    # ----------------------------------------
    # Attempt decryption
    # ----------------------------------------

    try:

        message = decrypt_message(
            encrypted_data,
            password
        )

        return message

    except Exception:

        return (
            "❌ Wrong password "
            "or corrupted data."
        )


# ========================================
# TEST RUN
# ========================================

if __name__ == "__main__":

    # Create random test image
    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (300, 300, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/secure_input.png"
    )

    # Secret message
    secret = (
        "FAANG recruiters cannot "
        "read this without password!"
    )

    password = "Manthan2026@Secret"

    # ----------------------------------------
    # Embed
    # ----------------------------------------

    result = secure_embed(

        "tests/test_images/secure_input.png",

        secret,

        password,

        "tests/test_images/secure_output.png"
    )

    print("\n=== EMBED RESULT ===")

    print(result)

    # ----------------------------------------
    # Correct password extraction
    # ----------------------------------------

    extracted = secure_extract(

        "tests/test_images/secure_output.png",

        password
    )

    print("\n=== EXTRACTED MESSAGE ===")

    print(extracted)

    # ----------------------------------------
    # Wrong password test
    # ----------------------------------------

    wrong = secure_extract(

        "tests/test_images/secure_output.png",

        "WrongPassword"
    )

    print("\n=== WRONG PASSWORD TEST ===")

    print(wrong)