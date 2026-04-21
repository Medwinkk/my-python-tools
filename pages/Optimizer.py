import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Premium JPEG Optimizer")
st.write("High-Fidelity Optimization: No Artifacts, No Metadata, Pure JPEG.")

files = st.file_uploader("Drag and drop images here", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)

if files:
    zip_buffer = io.BytesIO()
    total_old_size = 0
    total_new_size = 0

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            # Deschiderea imaginii si conversia la RGB pentru compatibilitate maxima
            img = Image.open(file).convert("RGB")
            
            # 1. Smart Sharpness: Daca imaginea e gigant, o scalam cu cel mai bun filtru (Lanczos)
            max_size = 2560
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            buf = io.BytesIO()
            
            # 2. Premium JPEG Settings:
            # quality=85 -> Balansul perfect unde artefactele sunt invizibile ochiului
            # subsampling=0 -> (4:4:4) Pastreaza culorile 100% clare (fara blur de compresie)
            # optimize=True -> Calculeaza tabele Huffman personalizate pentru fiecare poza
            img.save(
                buf, 
                format="JPEG", 
                quality=85, 
                subsampling=0, 
                optimize=True
            )
            
            total_old_size += file.size
            total_new_size += buf.getbuffer().nbytes
            
            # Adaugare in ZIP
            file_name = f"optimized_{file.name.split('.')[0]}.jpg"
            zip_file.writestr(file_name, buf.getvalue())

    reduction = 100 - (total_new_size / total_old_size * 100)
    
    st.subheader("Optimization Results")
    col1, col2 = st.columns(2)
    col1.metric("Initial Total", f"{total_old_size/1024/1024:.2f} MB")
    col2.metric("Final JPEG", f"{total_new_size/1024/1024:.2f} MB", f"-{reduction:.1f}%")
    
    st.success("Clean: All metadata (GPS, Camera info) has been stripped.")
    
    st.download_button(
        label=f"Download {len(files)} Optimized JPEGs (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="optimized_jpegs.zip",
        mime="application/zip"
    )
