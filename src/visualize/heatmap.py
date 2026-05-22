import cv2
import numpy as np

from PIL import Image

import matplotlib.pyplot as plt


def generate_heatmap(
    original_path: str,
    stego_path: str,
    output_path: str = None,
    amplify: int = 40
):

    """
    Generate visual heatmap
    showing hidden pixel changes
    """

    original = cv2.imread(
        original_path
    )

    stego = cv2.imread(
        stego_path
    )

    if original is None:

        raise ValueError(
            "Original image not found"
        )

    if stego is None:

        raise ValueError(
            "Stego image not found"
        )

    if original.shape != stego.shape:

        raise ValueError(
            "Image sizes differ"
        )

    # Absolute pixel difference
    diff = cv2.absdiff(
        original,
        stego
    )

    # Amplify tiny changes
    amplified = np.clip(
        diff * amplify,
        0,
        255
    ).astype(np.uint8)

    # Convert to grayscale intensity
    gray = cv2.cvtColor(
        amplified,
        cv2.COLOR_BGR2GRAY
    )

    # Apply heatmap coloring
    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    if output_path:

        cv2.imwrite(
            output_path,
            heatmap
        )

    return {

        "difference_pixels":
            int(np.count_nonzero(diff)),

        "max_difference":
            int(np.max(diff)),

        "mean_difference":
            round(float(np.mean(diff)), 4),

        "heatmap":
            heatmap
    }


def show_comparison(
    original_path: str,
    stego_path: str,
    amplify: int = 40
):

    """
    Display side-by-side comparison
    """

    result = generate_heatmap(

        original_path,

        stego_path,

        amplify=amplify
    )

    original = cv2.cvtColor(

        cv2.imread(original_path),

        cv2.COLOR_BGR2RGB
    )

    stego = cv2.cvtColor(

        cv2.imread(stego_path),

        cv2.COLOR_BGR2RGB
    )

    heatmap = cv2.cvtColor(

        result["heatmap"],

        cv2.COLOR_BGR2RGB
    )

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    axes[0].imshow(original)

    axes[0].set_title(
        "Original"
    )

    axes[1].imshow(stego)

    axes[1].set_title(
        "Stego"
    )

    axes[2].imshow(heatmap)

    axes[2].set_title(
        "Heatmap"
    )

    for ax in axes:

        ax.axis("off")

    plt.tight_layout()

    plt.show()

    print("\n📊 Heatmap Stats")

    print("-" * 30)

    print(
        f"Modified pixels: "
        f"{result['difference_pixels']}"
    )

    print(
        f"Max difference: "
        f"{result['max_difference']}"
    )

    print(
        f"Mean difference: "
        f"{result['mean_difference']}"
    )


if __name__ == "__main__":

    from src.embed.lsb_embed import (
        embed_message
    )

    # Create sample stego
    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (300, 300, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/heatmap_clean.png"
    )

    embed_message(

        "tests/test_images/heatmap_clean.png",

        "Very secret hidden message!",

        "tests/test_images/heatmap_stego.png"
    )

    # Generate heatmap
    show_comparison(

        "tests/test_images/heatmap_clean.png",

        "tests/test_images/heatmap_stego.png"
    )