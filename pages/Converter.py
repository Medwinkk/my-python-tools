import streamlit as st
from PIL import Image
import io

st.title("TIFF to JPEG Converter")
uploaded_file = st.file_uploader("Upload a TIFF image", type=["tif", "tiff"])

if uploaded_file:
    image = Image.open(uploaded_file)
    rgb_image = image.convert("RGB")
    buffer = io.BytesIO()
    rgb_image.save(buffer, format="JPEG", quality=95)
    st.image(image, caption="Original Image Preview")
    st.download_button(label="Download JPEG", data=buffer.getvalue(), file_name="converted.jpg", mime="image/jpeg")
