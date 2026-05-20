import ctypes
import os
import time

import numpy as np

from PIL import Image


# DLL path
LIB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "cpp",
    "lsb_fast.dll"
)

LIB_PATH = os.path.abspath(LIB_PATH)

_lib = None


def load_library():

    global _lib

    try:

        _lib = ctypes.CDLL(LIB_PATH)

        # embed_lsb
        _lib.embed_lsb.argtypes = [

            ctypes.POINTER(ctypes.c_uint8),

            ctypes.c_int,

            ctypes.c_char_p,

            ctypes.c_int
        ]

        _lib.embed_lsb.restype = ctypes.c_int

        # extract_lsb
        _lib.extract_lsb.argtypes = [

            ctypes.POINTER(ctypes.c_uint8),

            ctypes.c_int,

            ctypes.c_char_p,

            ctypes.c_int
        ]

        _lib.extract_lsb.restype = None

        # randomness score
        _lib.lsb_randomness_score.argtypes = [

            ctypes.POINTER(ctypes.c_uint8),

            ctypes.c_int
        ]

        _lib.lsb_randomness_score.restype = ctypes.c_double

        print("✅ C++ DLL loaded successfully")

        return True

    except Exception as e:

        print("❌ Failed to load DLL")
        print(e)

        return False


CPP_AVAILABLE = load_library()


def fast_embed(
    image_path: str,
    bits: str,
    output_path: str
):

    """
    Use C++ engine for fast embedding
    """

    img = Image.open(image_path).convert("RGB")

    pixels = np.array(
        img,
        dtype=np.uint8
    )

    flat = pixels.flatten()

    if CPP_AVAILABLE:

        ptr = flat.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        )

        result = _lib.embed_lsb(

            ptr,

            len(flat),

            bits.encode(),

            len(bits)
        )

        if result != 0:

            raise ValueError(
                "Image too small"
            )

    else:

        # Python fallback
        for i, bit in enumerate(bits):

            if i >= len(flat):

                break

            flat[i] = (
                flat[i] & 0xFE
            ) | int(bit)

    stego = Image.fromarray(
        flat.reshape(pixels.shape)
    )

    stego.save(output_path, "PNG")

    return True


def get_lsb_score(image_path: str):

    """
    Get LSB randomness score
    """

    img = Image.open(image_path).convert("RGB")

    pixels = np.array(
        img,
        dtype=np.uint8
    ).flatten()

    if CPP_AVAILABLE:

        ptr = pixels.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        )

        score = _lib.lsb_randomness_score(
            ptr,
            len(pixels)
        )

        return score

    return float(np.mean(pixels & 1))


def benchmark():

    """
    Benchmark Python vs C++
    """

    # Create large random image
    pixels = np.random.randint(

        0,
        255,
        (2000, 2000, 3),
        dtype=np.uint8
    )

    flat = pixels.flatten()

    bits = "01" * 500000

    # -----------------
    # Python benchmark
    # -----------------

    py_pixels = flat.copy()

    start = time.perf_counter()

    for i, bit in enumerate(bits):

        py_pixels[i] = (
            py_pixels[i] & 0xFE
        ) | int(bit)

    py_time = time.perf_counter() - start

    print(f"\nPython Time: {py_time:.4f}s")

    # -----------------
    # C++ benchmark
    # -----------------

    if CPP_AVAILABLE:

        cpp_pixels = flat.copy()

        ptr = cpp_pixels.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        )

        start = time.perf_counter()

        _lib.embed_lsb(

            ptr,

            len(cpp_pixels),

            bits.encode(),

            len(bits)
        )

        cpp_time = time.perf_counter() - start

        print(f"C++ Time: {cpp_time:.4f}s")

        speedup = py_time / cpp_time

        print(f"🚀 Speedup: {speedup:.2f}x")

    else:

        print("C++ DLL unavailable")


if __name__ == "__main__":

    benchmark()