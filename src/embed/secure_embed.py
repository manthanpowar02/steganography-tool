from src.embed.aes_encrypt import (
    encrypt_message,
    decrypt_message,
    bytes_to_bits,
    bits_to_bytes
)

from PIL import Image
import numpy as np
import struct


# Magic header
MAGIC_HEADER = b"STEG"


def secure_embed(
    image_path: str,
    message: str,
    password: str,
    output_path: str
) -> dict:

    """
    Encrypt message then embed into image
    """

    # Encrypt message
    encrypted_bytes = encrypt_message(
        message,
        password
    )

    # Add header + length
    payload = (
        MAGIC_HEADER
        + struct.pack(">I", len(encrypted_bytes))
        + encrypted_bytes
    )

    # Convert to bits
    binary_data = bytes_to_bits(payload)

    # Load image
    img = Image.open(image_path).convert("RGB")

    pixels = np.array(img)

    flat = pixels.flatten()

    # Capacity check
    if len(binary_data) > len(flat):

        raise ValueError(
            f"Image too small. Need {len(binary_data)} bits"
        )

    # Embed bits
    for i in range(len(binary_data)):

        flat[i] = (
            flat[i] & 0xFE
        ) | int(binary_data[i])

    # Save image
    stego_pixels = flat.reshape(pixels.shape)

    stego_img = Image.fromarray(
        stego_pixels.astype(np.uint8)
    )

    stego_img.save(output_path, "PNG")

    return {

        "status": "success",

        "message_length": len(message),

        "encrypted_size": len(encrypted_bytes),

        "bits_used": len(binary_data),

        "capacity_used_percent": round(
            len(binary_data) / len(flat) * 100,
            2
        ),

        "output": output_path
    }


def secure_extract(
    image_path: str,
    password: str
) -> str:

    """
    Extract encrypted data then decrypt
    """

    img = Image.open(image_path).convert("RGB")

    pixels = np.array(img)

    flat = pixels.flatten()

    # Extract LSBs
    bits = ""

    for pixel in flat:

        bits += str(pixel & 1)

    # Convert back to bytes
    extracted_bytes = bits_to_bytes(bits)

    # Verify header
    if extracted_bytes[:4] != MAGIC_HEADER:

        return "❌ No hidden encrypted content found"

    # Extract encrypted length
    data_length = struct.unpack(
        ">I",
        extracted_bytes[4:8]
    )[0]

    encrypted_data = extracted_bytes[
        8:8 + data_length
    ]

    # Try decryption
    try:

        message = decrypt_message(
            encrypted_data,
            password
        )

        return message

    except Exception:

        return "❌ Wrong password or corrupted data"


if __name__ == "__main__":

    from PIL import Image
    import numpy as np

    # Create sample image
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

    secret = (
        "FAANG recruiters cannot read this "
        "without the password!"
    )

    password = "Manthan2026@Secret"

    # Embed
    result = secure_embed(
        "tests/test_images/secure_input.png",
        secret,
        password,
        "tests/test_images/secure_output.png"
    )

    print("Embedded:")
    print(result)

    # Extract correctly
    extracted = secure_extract(
        "tests/test_images/secure_output.png",
        password
    )

    print("\nExtracted:")
    print(extracted)

    # Wrong password
    wrong = secure_extract(
        "tests/test_images/secure_output.png",
        "WrongPassword"
    )

    print("\nWrong password result:")
    print(wrong)