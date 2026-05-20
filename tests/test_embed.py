import pytest
from PIL import Image
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.embed.lsb_embed import (
    embed_message,
    extract_message,
    text_to_bits,
    bits_to_text
)

class TestLSBEmbed:

    def setup_method(self):
        """Create fresh image before every test"""

        img = Image.fromarray(
            np.random.randint(
                100,
                200,
                (100, 100, 3),
                dtype=np.uint8
            )
        )

        img.save("tests/test_images/test_clean.png")

    def test_embed_and_extract_short_message(self):

        original = "Hello World"

        embed_message(
            "tests/test_images/test_clean.png",
            original,
            "tests/test_images/test_stego.png"
        )

        extracted = extract_message(
            "tests/test_images/test_stego.png"
        )

        assert extracted == original

    def test_embed_and_extract_long_message(self):

        original = "A" * 200

        embed_message(
            "tests/test_images/test_clean.png",
            original,
            "tests/test_images/test_stego_long.png"
        )

        extracted = extract_message(
            "tests/test_images/test_stego_long.png"
        )

        assert extracted == original

    def test_stego_image_looks_identical(self):

        msg = "Secret"

        embed_message(
            "tests/test_images/test_clean.png",
            msg,
            "tests/test_images/test_visual.png"
        )

        original = np.array(
            Image.open("tests/test_images/test_clean.png")
        )

        stego = np.array(
            Image.open("tests/test_images/test_visual.png")
        )

        max_diff = np.max(
            np.abs(original.astype(int) - stego.astype(int))
        )

        assert max_diff <= 1

    def test_capacity_error_on_too_large_message(self):

        huge_message = "X" * 100000

        with pytest.raises(ValueError):

            embed_message(
                "tests/test_images/test_clean.png",
                huge_message,
                "tests/test_images/overflow.png"
            )

    def test_text_to_bits_conversion(self):

        assert text_to_bits("A") == "01000001"

    def test_bits_to_text_conversion(self):

        assert bits_to_text("01000001") == "A"