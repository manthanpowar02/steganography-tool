import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

from src.visualize.heatmap import (
    generate_heatmap
)

from src.embed.lsb_embed import (
    embed_message
)

from PIL import Image

import numpy as np


def test_heatmap_generation():

    img = Image.fromarray(

        np.random.randint(
            50,
            200,
            (200, 200, 3),
            dtype=np.uint8
        )
    )

    img.save(
        "tests/test_images/hm_clean.png"
    )

    embed_message(

        "tests/test_images/hm_clean.png",

        "Secret hidden message",

        "tests/test_images/hm_stego.png"
    )

    result = generate_heatmap(

        "tests/test_images/hm_clean.png",

        "tests/test_images/hm_stego.png"
    )

    assert result[
        "difference_pixels"
    ] > 0