import fitz
from io import BytesIO
from PIL import Image, ImageStat
import numpy as np

MIN_WIDTH = 200 
MIN_HEIGHT = 200
MIN_AREA_RATIO = 0.10 

def is_mostly_grayscale(image: Image.Image, threshold=15) -> bool:
    """
    Forma optimizada de detectar escala de grises sin recorrer pixel por pixel.
    Compara la diferencia entre canales usando ImageStat.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    stat = ImageStat.Stat(image)
    diff_rg = abs(stat.mean[0] - stat.mean[1])
    diff_rb = abs(stat.mean[0] - stat.mean[2])
    
    return diff_rg < threshold and diff_rb < threshold

def is_dark_background(image: Image.Image, threshold=60) -> bool:
    """
    FILTRO CLAVE: Las ecografías casi siempre tienen fondo negro.
    Los logos suelen tener fondo blanco.
    Revisamos las esquinas y los bordes.
    """
    gray = image.convert("L")
    width, height = gray.size
    
    corners = [
        (0, 0, 10, 10),
        (width-10, 0, width, 10),
        (0, height-10, 10, height),
        (width-10, height-10, width, height)
    ]
    
    dark_corners = 0
    for box in corners:
        region = gray.crop(box)
        stat = ImageStat.Stat(region)
        if stat.mean[0] < threshold:
            dark_corners += 1
            
    return dark_corners >= 3

def has_high_variance(image: Image.Image, threshold=20) -> bool:
    """
    FILTRO CLAVE 2: Distingue 'ruido' (ecografía) de 'plano' (logo).
    Las ecografías tienen una desviación estándar alta en sus píxeles.
    Los logos simples tienen desviación baja.
    """
    gray = image.convert("L")
    stat = ImageStat.Stat(gray)
    variance = stat.stddev[0]
    
    return variance > threshold

def extract_images(pdf_bytes: bytes) -> list[bytes]:
    images = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in doc:
        page_area = page.rect.width * page.rect.height

        for img_info in page.get_images(full=True):
            xref = img_info[0]
            
            if img_info[2] < MIN_WIDTH or img_info[3] < MIN_HEIGHT:
                continue

            base = doc.extract_image(xref)
            img_bytes = base["image"]
            
            try:
                image = Image.open(BytesIO(img_bytes))
            except Exception:
                continue

            width, height = image.size
            img_area = width * height

            ratio = width / height
            if not (0.5 < ratio < 2.0): 
                continue

            if img_area / page_area < MIN_AREA_RATIO:
                continue

            if not is_mostly_grayscale(image):
                continue

            if not is_dark_background(image):
                continue

            if not has_high_variance(image):
                continue

            buf = BytesIO()
            image.convert("RGB").save(buf, format="PNG") 
            images.append(buf.getvalue())

    return images