import re

def clean_text(raw_text: str) -> str:
    """
    Limpia texto extraído de OCR de PDFs heterogéneos.
    
    Pasos:
    - Normaliza saltos de línea
    - Elimina espacios en blanco redundantes
    - Quita caracteres extraños comunes del OCR
    - Devuelve un texto limpio listo para extracción estructurada
    """
  
    text = re.sub(r'\n+', '\n', raw_text)
    
    text = re.sub(r'[ \t]+', ' ', text)
    
    text = re.sub(r' *\n *', '\n', text)
    
    text = re.sub(r'[^\x00-\x7F]+', '', text)  
    text = re.sub(r'[^\w\s:.,()-]', '', text)  

    text = text.strip()
    
    return text
