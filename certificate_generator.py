from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import os

def draw_centered_text(draw, text, position, font, color=(0, 0, 0)):
    width, height = draw.textsize(text, font=font)
    position = (position[0] - width // 2, position[1] - height // 2)
    draw.text(position, text, fill=color, font=font)

def generate_certificate(name, course_name, date, template, font, font_small, output_dir):
    certificate = template.copy()
    draw = ImageDraw.Draw(certificate)

    name_pos = (certificate.width // 2, certificate.height // 2 - 140)
    course_date_pos = (certificate.width // 2, certificate.height // 2 - 40)
    msg_pos = (certificate.width // 2, certificate.height // 2 + 60)
    msg = "Congratulations for all your hard work, keep winning!"

    draw_centered_text(draw, name, name_pos, font)
    draw_centered_text(draw, f"{course_name} | {date}", course_date_pos, font_small)
    draw_centered_text(draw, msg, msg_pos, font_small)

    png_path = os.path.join(output_dir, f'{name}.png')
    pdf_path = os.path.join(output_dir, f'{name}.pdf')

    certificate.save(png_path)

    c = canvas.Canvas(pdf_path, pagesize=(template.width, template.height))
    c.drawImage(png_path, 0, 0, width=template.width, height=template.height)
    c.save()

    return pdf_path
