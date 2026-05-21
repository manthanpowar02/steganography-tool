from PIL import Image
import os


SUPPORTED_FORMATS = {
    ".png",
    ".bmp",
    ".tiff"
}

LOSSY_FORMATS = {
    ".jpg",
    ".jpeg"
}


def get_image_capacity(
    image_path: str
) -> dict:

    """
    Calculate maximum safe payload size
    """

    ext = os.path.splitext(
        image_path
    )[1].lower()

    # JPEG warning
    if ext in LOSSY_FORMATS:

        return {

            "can_use": False,

            "error":
                "JPEG uses lossy compression "
                "which destroys hidden LSB data. "
                "Please convert to PNG."
        }

    # Unsupported
    if ext not in SUPPORTED_FORMATS:

        return {

            "can_use": False,

            "error":
                f"Unsupported format: {ext}"
        }

    img = Image.open(
        image_path
    ).convert("RGB")

    width, height = img.size

    total_pixels = width * height

    total_channels = total_pixels * 3

    # Overhead:
    # magic header + AES IV + metadata
    overhead_bytes = 40

    usable_bytes = (
        total_channels // 8
    ) - overhead_bytes

    return {

        "can_use": True,

        "format": ext,

        "image_size":
            f"{width}x{height}",

        "total_pixels":
            total_pixels,

        "max_bytes":
            usable_bytes,

        "recommended_max":
            int(usable_bytes * 0.8),

        "channels":
            total_channels
    }


def convert_to_png(
    image_path: str
) -> str:

    """
    Convert lossy image to PNG
    """

    output = (
        image_path.rsplit(".", 1)[0]
        + "_converted.png"
    )

    img = Image.open(
        image_path
    ).convert("RGB")

    img.save(output, "PNG")

    print(f"✅ Converted to: {output}")

    return output


def validate_image(
    image_path: str
) -> bool:

    """
    Check image integrity
    """

    try:

        img = Image.open(image_path)

        img.verify()

        return True

    except Exception as e:

        print("❌ Invalid image")
        print(e)

        return False


if __name__ == "__main__":

    # Test image
    test_path = "tests/test_images/sample.png"

    print("\n--- VALIDATION ---")

    valid = validate_image(test_path)

    print(f"Valid: {valid}")

    print("\n--- CAPACITY ---")

    info = get_image_capacity(test_path)

    print(info)