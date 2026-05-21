"""
Generate benchmark dataset
"""

from PIL import Image

import numpy as np

import os
import sys

sys.path.insert(0, ".")

from src.embed.lsb_embed import (
    embed_message
)

# Create folders
os.makedirs(
    "tests/test_images/dataset/clean",
    exist_ok=True
)

os.makedirs(
    "tests/test_images/dataset/stego",
    exist_ok=True
)

messages = [

    "Short message",

    "A" * 100,

    "Hello FAANG!",

    "0123456789" * 20,

    "The quick brown fox jumps over the lazy dog."
]

print("\nGenerating dataset...")

for i in range(50):

    size = np.random.choice([
        100,
        150,
        200,
        250,
        300
    ])

    pattern = np.random.randint(0, 4)

    # Different image styles
    if pattern == 0:

        pixels = np.random.randint(

            0,
            255,
            (size, size, 3),
            dtype=np.uint8
        )

    elif pattern == 1:

        pixels = np.zeros(
            (size, size, 3),
            dtype=np.uint8
        )

        pixels[:, :, 0] = np.tile(
            np.arange(size) % 256,
            (size, 1)
        )

    elif pattern == 2:

        pixels = np.ones(
            (size, size, 3),
            dtype=np.uint8
        ) * (i * 5 % 255)

    else:

        x = np.linspace(
            0,
            255,
            size
        ).astype(np.uint8)

        pixels = np.outer(x, x).reshape(
            size,
            size,
            1
        )

        pixels = np.repeat(
            pixels[:, :, :1],
            3,
            axis=2
        )

    clean_path = (
        f"tests/test_images/dataset/clean/"
        f"clean_{i:03d}.png"
    )

    stego_path = (
        f"tests/test_images/dataset/stego/"
        f"stego_{i:03d}.png"
    )

    Image.fromarray(
        pixels
    ).save(clean_path)

    msg = messages[
        i % len(messages)
    ]

    try:

        embed_message(
            clean_path,
            msg,
            stego_path
        )

    except Exception:

        embed_message(
            clean_path,
            "short",
            stego_path
        )

print("\n✅ Dataset generated")

print("50 clean images")
print("50 stego images")