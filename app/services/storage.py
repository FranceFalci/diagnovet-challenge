import datetime
from google.cloud import storage
import google.auth
# from datetime import timedelta
import os
import logging
from dotenv import load_dotenv
from google.auth import impersonated_credentials


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
        sa_email = os.environ.get("SERVICE_ACCOUNT_EMAIL")
        
        logger.info(f"Intentando firmar URL para: {blob_name}")
        
        if not sa_email:
            raise ValueError("Falta SERVICE_ACCOUNT_EMAIL")

        source_credentials, project_id = google.auth.default()

        signer_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=sa_email,
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=minutes * 60
        )

        client = storage.Client(credentials=signer_credentials)
        
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=minutes),
            method="GET",
        )
        
        logger.info(f"URL Generada con éxito: {url[:30]}...")
        return url

    except Exception as e:
        logger.error(f"!!! ERROR FINAL: {str(e)}")
        raise e