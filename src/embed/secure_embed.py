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

    # -----------------------------
    # Validate image format/capacity
    # -----------------------------

    capacity = get_image_capacity(image_path)

    if not capacity["can_use"]:

        raise ValueError(
            capacity["error"]
        )

    # -----------------------------
    # Encrypt message
    # -----------------------------

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

    # -----------------------------
    # Capacity check
    # -----------------------------

    if len(binary_data) > len(flat):

        raise ValueError(
            f"Image too small. Need {len(binary_data)} bits"
        )

    # -----------------------------
    # Embed bits
    # -----------------------------

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