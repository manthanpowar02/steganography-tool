import numpy as np

from PIL import Image


def rs_analysis(
    image_path: str
) -> dict:

    """
    RS Analysis
    """

    img = Image.open(
        image_path
    ).convert("L")

    pixels = np.array(
        img,
        dtype=np.uint8
    )

    group_size = 4

    h, w = pixels.shape

    R = S = U = 0

    Rn = Sn = Un = 0

    flip_mask = np.array([0, 1, 0, 1])

    for i in range(h):

        for j in range(
            0,
            w - group_size + 1,
            group_size
        ):

            group = pixels[
                i,
                j:j + group_size
            ].copy()

            noise_orig = measure_noise(group)

            # Positive flip
            g1 = group.copy()

            for k in range(group_size):

                if flip_mask[k]:

                    g1[k] = g1[k] ^ 1

            noise_f1 = measure_noise(g1)

            # Negative flip
            gn = group.copy()

            for k in range(group_size):

                if flip_mask[k]:

                    gn[k] = (
                        (gn[k] - 1) ^ 1
                    )

            noise_fn = measure_noise(gn)

            # Classify
            if noise_f1 > noise_orig:

                R += 1

            elif noise_f1 < noise_orig:

                S += 1

            else:

                U += 1

            if noise_fn > noise_orig:

                Rn += 1

            elif noise_fn < noise_orig:

                Sn += 1

            else:

                Un += 1

    total = R + S + U

    if total == 0:

        return {

            "error":
                "No groups processed"
        }

    r_ratio = R / total

    rn_ratio = Rn / total

    s_ratio = S / total

    sn_ratio = Sn / total

    asymmetry = abs(

        (r_ratio - rn_ratio)

        -

        (s_ratio - sn_ratio)
    )

    confidence = min(
        100,
        int(asymmetry * 300)
    )

    return {

        "method":
            "RS Analysis",

        "R": R,
        "S": S,
        "R_neg": Rn,
        "S_neg": Sn,

        "asymmetry":
            round(asymmetry, 4),

        "confidence":
            confidence,

        "verdict":
            verdict(confidence)
    }


def measure_noise(group):

    return sum(

        abs(

            int(group[i])

            -

            int(group[i - 1])

        )

        for i in range(1, len(group))
    )


def verdict(c):

    if c < 20:

        return "✅ CLEAN"

    elif c < 50:

        return "🟡 SUSPICIOUS"

    elif c < 75:

        return "🟠 LIKELY STEGO"

    return "🔴 STEGO DETECTED"