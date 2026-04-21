import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Batch Pro Optimizer")
st.write("Drag multiple files to strip metadata and optimize colors.")

files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    total_old_size = 0
    total_new_size = 0

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            img = Image.open(file).convert("RGB")
            
            # Pro Optimization logic
            optimized_img = img.quantize(colors=256, method=2).convert("RGB")
            
            buf = io.BytesIO()
            optimized_img.save(buf, format="JPEG", optimize=True, quality=80, subsampling=0)
            
            # Statistics
            total_old_size += file.size
            total_new_size += buf.getbuffer().nbytes
            
            # Add to ZIP
            zip_file.writestr(f"opt_{file.name.split('.')[0]}.jpg", buf.getvalue())

    reduction = 100 - (total_new_size / total_old_size * 100)
    st.metric("Total Space Saved", f"{total_new_size/1024/1024:.2f} MB", f"-{reduction:.1f}%")
    
    st.download_button(
        label=f"Download {len(files)} Optimized Files (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="optimized_batch.zip",
        mime="application/zip"
    )
