import numpy as np

from PIL import Image

from scipy.stats import chi2


def chi_square_attack(
    image_path: str
) -> dict:

    """
    Chi-Square steganalysis
    """

    img = Image.open(
        image_path
    ).convert("RGB")

    pixels = np.array(
        img,
        dtype=np.uint8
    ).flatten()

    # Count frequencies
    observed = np.bincount(
        pixels,
        minlength=256
    ).astype(float)

    chi_stat = 0.0

    pairs_used = 0

    for k in range(128):

        o1 = observed[2 * k]

        o2 = observed[2 * k + 1]

        expected = (o1 + o2) / 2

        if expected > 5:

            chi_stat += (

                ((o1 - expected) ** 2)

                +

                ((o2 - expected) ** 2)

            ) / expected

            pairs_used += 2

    if pairs_used == 0:

        return {

            "error":
                "Insufficient data"
        }

    dof = pairs_used - 1

    p_value = 1 - chi2.cdf(
        chi_stat,
        dof
    )

    confidence = int(
        (1 - p_value) * 100
    )

    return {

        "method":
            "Chi-Square Attack",

        "chi_statistic":
            round(chi_stat, 2),

        "p_value":
            round(p_value, 6),

        "confidence":
            confidence,

        "verdict":
            verdict(confidence)
    }


def verdict(c):

    if c < 20:

        return "✅ CLEAN"

    elif c < 50:

        return "🟡 SUSPICIOUS"

    elif c < 75:

        return "🟠 LIKELY STEGO"

    return "🔴 STEGO DETECTED"