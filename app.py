import streamlit as st

import tempfile
import os

from PIL import Image

from src.embed.secure_embed import (
    secure_embed,
    secure_extract
)

from src.detect.ensemble import (
    full_detection
)

from src.visualize.heatmap import (
    generate_heatmap
)

from src.embed.image_utils import (
    get_image_capacity
)

st.set_page_config(

    page_title=
    "Steganography Attack & Detection Toolkit",

    layout="wide"
)

# -------------------------
# TITLE
# -------------------------

st.title(
    "🛡️ Steganography Attack & Detection Toolkit"
)

st.markdown("""

Hybrid Cybersecurity Toolkit featuring:

- AES-256 encrypted steganography
- LSB statistical analysis
- Chi-Square attack
- RS analysis
- Ensemble detection
- Heatmap visualization
- Python + C++ acceleration

""")

# -------------------------
# SIDEBAR
# -------------------------

mode = st.sidebar.selectbox(

    "Select Mode",

    [

        "Embed Secret Message",

        "Extract Secret Message",

        "Analyze Image",

        "Heatmap Visualization"
    ]
)

# -------------------------
# EMBED MODE
# -------------------------

if mode == "Embed Secret Message":

    st.header(
        "🔐 Embed Secret Message"
    )

    uploaded = st.file_uploader(

        "Upload image",

        type=[
            "png",
            "bmp",
            "tiff"
        ]
    )

    message = st.text_area(
        "Secret Message"
    )

    password = st.text_input(

        "Password",

        type="password"
    )

    if uploaded:

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".png"
        ) as tmp:

            tmp.write(uploaded.read())

            input_path = tmp.name

        info = get_image_capacity(
            input_path
        )

        st.info(info)

        if st.button(
            "Embed Message"
        ):

            output_path = (
                input_path.replace(
                    ".png",
                    "_stego.png"
                )
            )

            try:

                result = secure_embed(

                    input_path,

                    message,

                    password,

                    output_path
                )

                st.success(
                    "Message embedded successfully"
                )

                st.json(result)

                with open(
                    output_path,
                    "rb"
                ) as f:

                    st.download_button(

                        "⬇ Download Stego Image",

                        f,

                        file_name=
                        "stego_image.png"
                    )

            except Exception as e:

                st.error(str(e))

# -------------------------
# EXTRACT MODE
# -------------------------

elif mode == "Extract Secret Message":

    st.header(
        "🔓 Extract Secret Message"
    )

    uploaded = st.file_uploader(

        "Upload stego image",

        type=[
            "png",
            "bmp",
            "tiff"
        ]
    )

    password = st.text_input(

        "Password",

        type="password"
    )

    if uploaded:

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".png"
        ) as tmp:

            tmp.write(uploaded.read())

            path = tmp.name

        if st.button(
            "Extract Message"
        ):

            result = secure_extract(
                path,
                password
            )

            st.text_area(
                "Extracted Message",
                result,
                height=200
            )

# -------------------------
# ANALYZE MODE
# -------------------------

elif mode == "Analyze Image":

    st.header(
        "🕵️ Steganalysis"
    )

    uploaded = st.file_uploader(

        "Upload image",

        type=[
            "png",
            "bmp",
            "tiff"
        ]
    )

    if uploaded:

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".png"
        ) as tmp:

            tmp.write(uploaded.read())

            path = tmp.name

        if st.button(
            "Analyze Image"
        ):

            with st.spinner(
                "Running detection algorithms..."
            ):

                result = full_detection(path)

            st.subheader(
                result["final_verdict"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "LSB Analysis",

                    f"{result['lsb']['confidence']}%"
                )

            with col2:

                st.metric(

                    "Chi-Square",

                    f"{result['chi_square']['confidence']}%"
                )

            with col3:

                st.metric(

                    "RS Analysis",

                    f"{result['rs_analysis']['confidence']}%"
                )

            st.json(result)

# -------------------------
# HEATMAP MODE
# -------------------------

elif mode == "Heatmap Visualization":

    st.header(
        "🔥 Heatmap Visualization"
    )

    original = st.file_uploader(

        "Original Image",

        type=["png"]
    )

    stego = st.file_uploader(

        "Stego Image",

        type=["png"]
    )

    if original and stego:

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".png"
        ) as tmp1:

            tmp1.write(original.read())

            original_path = tmp1.name

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".png"
        ) as tmp2:

            tmp2.write(stego.read())

            stego_path = tmp2.name

        if st.button(
            "Generate Heatmap"
        ):

            output = (
                original_path.replace(
                    ".png",
                    "_heatmap.png"
                )
            )

            result = generate_heatmap(

                original_path,

                stego_path,

                output
            )

            st.image(

                output,

                caption="Heatmap"
            )

            st.json({

                "difference_pixels":
                    result["difference_pixels"],

                "max_difference":
                    result["max_difference"],

                "mean_difference":
                    result["mean_difference"]
            })