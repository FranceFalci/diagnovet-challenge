import datetime
from google.cloud import storage
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()
sa_email = os.environ.get("SERVICE_ACCOUNT_EMAIL") 
client = storage.Client()

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
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="GET",
        service_account_email=sa_email
    )
    return url
