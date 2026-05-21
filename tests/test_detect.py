import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.detect.lsb_detect import (
    analyze_lsb_distribution
)

from src.embed.lsb_embed import (
    embed_message
)

from PIL import Image

import numpy as np


def test_detect_stego_image():

    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/test_detect_clean.png"
    )

    large_message = "A" * 5000

    embed_message(
    "tests/test_images/test_detect_clean.png",
    large_message,
    "tests/test_images/test_detect_stego.png"
)

    result = analyze_lsb_distribution(

        "tests/test_images/test_detect_stego.png"
    )

    assert result["confidence"] >= 20


def test_detect_clean_image():

    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/test_clean_only.png"
    )

    result = analyze_lsb_distribution(

        "tests/test_images/test_clean_only.png"
    )

    assert result["confidence"] < 50