from pdf2image import convert_from_bytes
import io

def extract_images(pdf_bytes: bytes):
    images = convert_from_bytes(pdf_bytes)
    image_bytes = []

    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        image_bytes.append(buf.getvalue())

    return image_bytes
