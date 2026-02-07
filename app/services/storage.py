# app/services/storage.py
from google.cloud import storage
import uuid

client = storage.Client()

def upload_pdf(file_bytes: bytes, filename: str, bucket_name: str):
    bucket = client.bucket(bucket_name)
    blob_name = f"reports/{uuid.uuid4()}_{filename}"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(file_bytes, content_type="application/pdf")
    return blob_name
