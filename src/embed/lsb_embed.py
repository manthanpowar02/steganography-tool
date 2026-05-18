from PIL import Image
import numpy as np

def text_to_bits(text: str) -> str:
    """Convert text to binary"""
    bits = ""
    for char in text:
        bits += format(ord(char), '08b')
    return bits

def bits_to_text(bits: str) -> str:
    """Convert binary to text"""
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def embed_message(image_path: str, message: str, output_path: str):
    """
    Hide message inside image using LSB
    """

    # Open image
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    # Add end marker
    message += "###END###"

    # Convert message to bits
    binary_message = text_to_bits(message)

    # Flatten image array
    flat_pixels = pixels.flatten()

    # Capacity check
    if len(binary_message) > len(flat_pixels):
        raise ValueError("Message too large for image")

    # Embed bits
    for i in range(len(binary_message)):
        flat_pixels[i] = (
            flat_pixels[i] & 0xFE
        ) | int(binary_message[i])

    # Reshape back
    stego_pixels = flat_pixels.reshape(pixels.shape)

    # Save image
    stego_img = Image.fromarray(stego_pixels.astype(np.uint8))
    stego_img.save(output_path, "PNG")

    print("✅ Message embedded successfully")

def extract_message(image_path: str):
    """
    Extract hidden message
    """

    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)

    flat_pixels = pixels.flatten()

    # Extract LSBs
    bits = ""
    for pixel in flat_pixels:
        bits += str(pixel & 1)

    # Convert to text
    extracted = bits_to_text(bits)

    # Find end marker
    end_marker = "###END###"

    if end_marker in extracted:
        extracted = extracted[:extracted.index(end_marker)]

    return extracted

if __name__ == "__main__":

    # Test image path
    input_image = "tests/test_images/sample.png"

    # Output image path
    output_image = "tests/test_images/stego.png"

    # Secret message
    secret_message = "Hello Manthan! Hidden Message."

    # Embed
    embed_message(
        input_image,
        secret_message,
        output_image
    )

    # Extract
    extracted = extract_message(output_image)

    print("Extracted Message:")
    print(extracted)