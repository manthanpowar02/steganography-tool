import numpy as np

from PIL import Image


def analyze_lsb_distribution(
    image_path: str
) -> dict:

    """
    Analyze LSB statistical distribution
    """

    img = Image.open(
        image_path
    ).convert("RGB")

    pixels = np.array(
        img,
        dtype=np.uint8
    )

    # Extract LSBs
    r_lsb = pixels[:, :, 0] & 1
    g_lsb = pixels[:, :, 1] & 1
    b_lsb = pixels[:, :, 2] & 1

    all_lsb = np.concatenate([

        r_lsb.flatten(),

        g_lsb.flatten(),

        b_lsb.flatten()
    ])

    total_bits = len(all_lsb)

    ones = int(np.sum(all_lsb))

    zeros = total_bits - ones

    ratio = ones / total_bits

    # Ideal random ≈ 0.5
    deviation = abs(ratio - 0.5)

    # Run analysis
    runs = count_runs(all_lsb)

    expected_runs = (

        (2 * ones * zeros) / total_bits
    ) + 1

    run_ratio = runs / expected_runs

    # Confidence scoring
    confidence = min(
    100,
    int(
        deviation * 500
        + abs(run_ratio - 1) * 30
    )
)

    return {
    "method": "LSB Statistical Analysis",

    "lsb_ratio": round(ratio, 4),

    "deviation": round(deviation, 4),

    "ones": ones,

    "zeros": zeros,

    "runs": runs,

    "expected_runs": round(expected_runs, 2),

    "run_ratio": round(run_ratio, 4),

    "confidence": confidence,

    "verdict": verdict(confidence)
}


def count_runs(bit_array):
    """
    Count consecutive bit runs
    """

    if len(bit_array) == 0:

        return 0

    runs = 1

    for i in range(1, len(bit_array)):

        if bit_array[i] != bit_array[i - 1]:

            runs += 1

    return runs


def verdict(
    confidence: int
):

    if confidence < 20:

        return "✅ CLEAN"

    elif confidence < 50:

        return "🟡 SUSPICIOUS"

    elif confidence < 75:

        return "🟠 LIKELY STEGO"

    return "🔴 STEGO DETECTED"


if __name__ == "__main__":

    from src.embed.lsb_embed import (
        embed_message
    )

    from PIL import Image

    import numpy as np

    # Create clean image
    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/detect_clean.png"
    )

    # Create stego image
    embed_message(
    "tests/test_images/detect_clean.png",
    "A" * 5000,
    "tests/test_images/detect_stego.png"
)

    # Analyze clean
    print("\n--- CLEAN IMAGE ---")

    clean = analyze_lsb_distribution(
        "tests/test_images/detect_clean.png"
    )

    print(clean)

    # Analyze stego
    print("\n--- STEGO IMAGE ---")

    stego = analyze_lsb_distribution(
        "tests/test_images/detect_stego.png"
    )

    print(stego)