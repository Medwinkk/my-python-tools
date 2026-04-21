import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Batch TIFF to JPEG")

files = st.file_uploader("Drag and drop TIFF images here", type=["tif", "tiff"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            img = Image.open(file).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95)
            # Add to ZIP
            zip_file.writestr(f"{file.name.split('.')[0]}.jpg", buf.getvalue())
            
    st.success(f"Processed {len(files)} files.")
    st.download_button(
        label="Download All as ZIP",
        data=zip_buffer.getvalue(),
        file_name="converted_images.zip",
        mime="application/zip"
    )
