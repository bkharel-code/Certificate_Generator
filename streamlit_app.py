import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from reportlab.pdfgen import canvas

# Page config
st.set_page_config(page_title="Certificate Generator", layout="centered")
st.title("🏅 Student of the Month Certificate Generator")

st.markdown("Upload a certificate template, a font file, and a data file (name, course, date).")

# File uploaders
uploaded_template = st.file_uploader("🖼️ Upload Certificate Template (PNG)", type=["png"])
uploaded_font = st.file_uploader("🔤 Upload Font (TTF)", type=["ttf"])
uploaded_data = st.file_uploader("📄 Upload Data File (TXT)", type=["txt"])

if uploaded_template and uploaded_font and uploaded_data:
    with st.spinner("Processing certificates..."):

        # Save font to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font:
            tmp_font.write(uploaded_font.read())
            font_path = tmp_font.name

        # Load font
        font_large = ImageFont.truetype(font_path, 60)
        font_small = ImageFont.truetype(font_path, 40)

        # Load template
        template = Image.open(uploaded_template)

        # Read data file
        entries = []
        for line in uploaded_data.read().decode("utf-8").splitlines():
            parts = line.strip().split(",")
            if len(parts) == 3:
                name, course, date = [p.strip() for p in parts]
                entries.append((name, course, date))

        # Prepare output directory
        output_dir = tempfile.mkdtemp()

        # Drawing helper
        def draw_centered(draw, text, position, font, color=(0, 0, 0)):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            pos = (position[0] - w // 2, position[1] - h // 2)
            draw.text(pos, text, fill=color, font=font)

        # Generate certificates
        for name, course, date in entries:
            cert_img = template.copy()
            draw = ImageDraw.Draw(cert_img)

            draw_centered(draw, name, (cert_img.width // 2, cert_img.height // 2 - 140), font_large)
            draw_centered(draw, f"{course} | {date}", (cert_img.width // 2, cert_img.height // 2 - 40), font_small)
            draw_centered(draw, "Congratulations for all your hard work, keep winning!",
                          (cert_img.width // 2, cert_img.height // 2 + 60), font_small)

            # Save PNG
            output_png = os.path.join(output_dir, f"{name}_certificate.png")
            cert_img.save(output_png)

            # Save PDF
            output_pdf = os.path.join(output_dir, f"{name}_certificate.pdf")
            c = canvas.Canvas(output_pdf, pagesize=(cert_img.width, cert_img.height))
            c.drawImage(output_png, 0, 0, width=cert_img.width, height=cert_img.height)
            c.save()

        st.success(f"✅ Generated {len(entries)} certificates!")

        # Download ZIP
        import zipfile
        zip_path = os.path.join(output_dir, "certificates.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in os.listdir(output_dir):
                if filename.endswith(".pdf"):
                    zipf.write(os.path.join(output_dir, filename), arcname=filename)

        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download All Certificates (ZIP)", f, file_name="certificates.zip")

else:
    st.info("Please upload all three files to begin.")
