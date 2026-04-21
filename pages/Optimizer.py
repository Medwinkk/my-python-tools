import streamlit as st
from PIL import Image
import io

st.title("Pro Image Optimizer")
st.write("Metadata stripping + Color Quantization (JPEG Mini style)")

uploaded_file = st.file_uploader("Upload image (JPG, PNG, TIFF)", type=["jpg", "jpeg", "png", "tif", "tiff"])

if uploaded_file:
    original_img = Image.open(uploaded_file).convert("RGB")
    
    # Reducem culorile (Quantization) pentru a optimiza spatiul
    optimized_img = original_img.quantize(colors=256, method=2).convert("RGB")
    
    buffer = io.BytesIO()
    # Salvam fara metadata (EXIF) si cu optimizare Huffman
    optimized_img.save(buffer, format="JPEG", optimize=True, quality=80, subsampling=0)
    
    st.subheader("Results")
    reduction = 100 - (buffer.getbuffer().nbytes / uploaded_file.size * 100)
    st.metric("New Size", f"{buffer.getbuffer().nbytes / 1024:.2f} KB", f"-{reduction:.1f}%")
    st.info("Privacy Shield: All EXIF/GPS metadata has been removed.")
    
    st.download_button(label="Download Optimized Image", data=buffer.getvalue(), file_name="optimized.jpg", mime="image/jpeg")
