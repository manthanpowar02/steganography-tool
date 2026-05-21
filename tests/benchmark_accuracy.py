"""
Benchmark all detection algorithms
"""

import os
import sys

sys.path.insert(0, ".")

from src.detect.ensemble import (
    full_detection
)

clean_dir = (
    "tests/test_images/dataset/clean"
)

stego_dir = (
    "tests/test_images/dataset/stego"
)

results = {

    "lsb": {
        "tp": 0,
        "tn": 0,
        "fp": 0,
        "fn": 0
    },

    "chi": {
        "tp": 0,
        "tn": 0,
        "fp": 0,
        "fn": 0
    },

    "rs": {
        "tp": 0,
        "tn": 0,
        "fp": 0,
        "fn": 0
    },

    "ensemble": {
        "tp": 0,
        "tn": 0,
        "fp": 0,
        "fn": 0
    }
}


def classify(
    confidence,
    threshold=50
):

    return (
        "stego"
        if confidence >= threshold
        else "clean"
    )


print("\nRunning benchmark...")

# -----------------------------
# CLEAN IMAGES
# -----------------------------

for fname in os.listdir(clean_dir):

    path = os.path.join(
        clean_dir,
        fname
    )

    try:

        result = full_detection(path)

        # LSB
        pred = classify(
            result["lsb"]["confidence"]
        )

        if pred == "clean":

            results["lsb"]["tn"] += 1

        else:

            results["lsb"]["fp"] += 1

        # CHI
        pred = classify(
            result["chi_square"]["confidence"]
        )

        if pred == "clean":

            results["chi"]["tn"] += 1

        else:

            results["chi"]["fp"] += 1

        # RS
        pred = classify(
            result["rs_analysis"]["confidence"]
        )

        if pred == "clean":

            results["rs"]["tn"] += 1

        else:

            results["rs"]["fp"] += 1

        # ENSEMBLE
        pred = classify(
            result["ensemble_confidence"]
        )

        if pred == "clean":

            results["ensemble"]["tn"] += 1

        else:

            results["ensemble"]["fp"] += 1

    except Exception:

        pass


# -----------------------------
# STEGO IMAGES
# -----------------------------

for fname in os.listdir(stego_dir):

    path = os.path.join(
        stego_dir,
        fname
    )

    try:

        result = full_detection(path)

        # LSB
        pred = classify(
            result["lsb"]["confidence"]
        )

        if pred == "stego":

            results["lsb"]["tp"] += 1

        else:

            results["lsb"]["fn"] += 1

        # CHI
        pred = classify(
            result["chi_square"]["confidence"]
        )

        if pred == "stego":

            results["chi"]["tp"] += 1

        else:

            results["chi"]["fn"] += 1

        # RS
        pred = classify(
            result["rs_analysis"]["confidence"]
        )

        if pred == "stego":

            results["rs"]["tp"] += 1

        else:

            results["rs"]["fn"] += 1

        # ENSEMBLE
        pred = classify(
            result["ensemble_confidence"]
        )

        if pred == "stego":

            results["ensemble"]["tp"] += 1

        else:

            results["ensemble"]["fn"] += 1

    except Exception:

        pass


# -----------------------------
# METRICS
# -----------------------------

print("\n📊 BENCHMARK RESULTS")
print("-" * 60)

print(
    f"{'Algorithm':<15}"
    f"{'Accuracy':>12}"
    f"{'Precision':>12}"
    f"{'Recall':>12}"
)

print("-" * 60)

for name, key in [

    ("LSB", "lsb"),

    ("Chi-Square", "chi"),

    ("RS", "rs"),

    ("Ensemble", "ensemble")
]:

    r = results[key]

    total = (
        r["tp"]
        + r["tn"]
        + r["fp"]
        + r["fn"]
    )

    accuracy = (

        (r["tp"] + r["tn"])
        / total
    ) * 100

    precision = (

        r["tp"]
        / (r["tp"] + r["fp"] + 1e-9)
    ) * 100

    recall = (

        r["tp"]
        / (r["tp"] + r["fn"] + 1e-9)
    ) * 100

    print(

        f"{name:<15}"

        f"{accuracy:>10.1f}%"

        f"{precision:>11.1f}%"

        f"{recall:>11.1f}%"
    )

print("-" * 60)