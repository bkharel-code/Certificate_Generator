import streamlit as st
import pandas as pd
from PIL import ImageFont, Image
import zipfile
import tempfile
import os

from deploy import generate_certificate  # import your function

st.title("🎓 Certificate Generator")

uploaded_file = st.file_uploader("Upload a CSV or TXT (name, course, date)", type=["csv", "txt"])
template_file = st.file_uploader("Upload Certificate Template (PNG)", type=["png"])
font_file = st.file_uploader("Upload Font File (TTF)", type=["ttf"])

if uploaded_file and template_file and font_file:
    font = ImageFont.truetype(font_file, 60)
    font_small = ImageFont.truetype(font_file, 40)
    template = Image.open(template_file)

    # Parse uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file, names=["Name", "Course", "Date"])

    st.write("Preview:", df.head())

    if st.button("Generate Certificates"):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_paths = []
            for _, row in df.iterrows():
                pdf_path = generate_certificate(
                    name=row["Name"],
                    course_name=row["Course"],
                    date=row["Date"],
                    template=template,
                    font=font,
                    font_small=font_small,
                    output_dir=tmpdir
                )
                pdf_paths.append(pdf_path)

            # Create ZIP
            zip_path = os.path.join(tmpdir, "certificates.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for pdf in pdf_paths:
                    zipf.write(pdf, arcname=os.path.basename(pdf))

            with open(zip_path, "rb") as f:
                st.download_button("Download All Certificates as ZIP", f.read(), "certificates.zip")
