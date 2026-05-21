import os
import sys
import numpy as np

from PIL import Image

# Add project root to path
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

from src.detect.ensemble import (
    full_detection
)

from src.embed.lsb_embed import (
    embed_message
)


def test_detect_stego_image():

    # Create random clean image
    img = Image.fromarray(
        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    clean_path = (
        "tests/test_images/test_detect_clean.png"
    )

    stego_path = (
        "tests/test_images/test_detect_stego.png"
    )

    img.save(clean_path)

    # Large payload for reliable detection
    large_message = "A" * 5000

    # Embed hidden message
    embed_message(
        clean_path,
        large_message,
        stego_path
    )

    # Analyze stego image
    result = analyze_lsb_distribution(
        stego_path
    )

    print("\nStego Detection Result:")
    print(result)

    # Detector should notice changes
    assert result["confidence"] >= 20


def test_detect_clean_image():

    # Create random clean image
    img = Image.fromarray(
        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    clean_path = (
        "tests/test_images/test_clean_only.png"
    )

    img.save(clean_path)

    # Analyze untouched image
    result = analyze_lsb_distribution(
        clean_path
    )

    print("\nClean Detection Result:")
    print(result)

    # Clean image should not look suspicious
    assert result["confidence"] < 50


def test_ensemble_detection():

    # Create clean image
    img = Image.fromarray(
        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    clean_path = (
        "tests/test_images/ensemble_clean.png"
    )

    stego_path = (
        "tests/test_images/ensemble_stego.png"
    )

    img.save(clean_path)

    # Large payload
    large_message = "B" * 5000

    # Embed hidden data
    embed_message(
        clean_path,
        large_message,
        stego_path
    )

    # Run ensemble detector
    result = full_detection(
        stego_path
    )

    print("\nEnsemble Detection Result:")
    print(result)

    # Ensemble should detect stego artifacts
    assert result["ensemble_confidence"] >= 20