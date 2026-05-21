from src.detect.lsb_detect import (
    analyze_lsb_distribution
)

from src.detect.chi_square import (
    chi_square_attack
)

from src.detect.rs_analysis import (
    rs_analysis
)


def full_detection(
    image_path: str
) -> dict:

    """
    Run all detection algorithms
    """

    lsb = analyze_lsb_distribution(
        image_path
    )

    chi = chi_square_attack(
        image_path
    )

    rs = rs_analysis(
        image_path
    )

    lsb_c = lsb.get("confidence", 0)

    chi_c = chi.get("confidence", 0)

    rs_c = rs.get("confidence", 0)

    # Weighted ensemble
    ensemble = int(

        lsb_c * 0.25

        +

        chi_c * 0.45

        +

        rs_c * 0.30
    )

    votes = sum(

        1 for c in [
            lsb_c,
            chi_c,
            rs_c
        ]

        if c >= 50
    )

    return {

        "lsb": lsb,

        "chi_square": chi,

        "rs_analysis": rs,

        "ensemble_confidence":
            ensemble,

        "votes_for_stego":
            f"{votes}/3",

        "final_verdict":
            final_verdict(
                ensemble,
                votes
            )
    }


def final_verdict(
    confidence,
    votes
):

    if confidence >= 70 or votes >= 2:

        return (
            f"🔴 STEGO DETECTED "
            f"({confidence}% confidence)"
        )

    elif confidence >= 40:

        return (
            f"🟡 SUSPICIOUS "
            f"({confidence}% confidence)"
        )

    return (
        f"✅ CLEAN "
        f"({confidence}% confidence)"
    )