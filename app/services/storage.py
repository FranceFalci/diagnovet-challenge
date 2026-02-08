import datetime
from google.cloud import storage
from datetime import timedelta
import os
import logging
from dotenv import load_dotenv
load_dotenv()
client = storage.Client()
logger = logging.getLogger("uvicorn.error")

def upload_pdf(file_bytes: bytes, filename: str, bucket_name: str, report_id: str):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"reports/{report_id}/original.pdf")
    blob.upload_from_string(file_bytes, content_type="application/pdf")
    return blob.name

def upload_image(image_bytes: bytes, bucket_name: str, report_id: str, index: int):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"reports/{report_id}/images/image_{index}.png")
    blob.upload_from_string(image_bytes, content_type="image/png")
    return blob.name

def generate_signed_url(bucket_name: str, blob_name: str, minutes: int = 15):
    try:
        # --- DEBUG START ---
        sa_email = os.environ.get("SERVICE_ACCOUNT_EMAIL")
        
        logger.info("============== DEBUG START ==============")
        logger.info(f"Generando URL para Bucket: '{bucket_name}' / Blob: '{blob_name}'")
        logger.info(f"Valor de SERVICE_ACCOUNT_EMAIL: '{sa_email}'")
        
        # Verificación explícita
        if not sa_email:
            logger.error("!!! ERROR CRITICO: La variable de entorno SERVICE_ACCOUNT_EMAIL está VACIA o es None.")
            logger.error("Esto causará que google-storage intente usar credenciales locales y falle.")
        else:
            logger.info("El email existe, intentando firmar vía IAM...")
        # --- DEBUG END ---

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=minutes),
            method="GET",
            service_account_email=sa_email,
            access_token=None # Forzamos a que no busque tokens locales
        )
        
        logger.info(f"SUCCESS: URL generada correctamente (empieza con {url[:15]}...)")
        return url

    except Exception as e:
        logger.error(f"!!! EXCEPCION AL FIRMAR URL: {str(e)}")
        # Re-lanzamos el error para que la app responda 500, pero ya quedó registrado en logs
        raise e
