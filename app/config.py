# app/config.py
import os
from dotenv import load_dotenv
load_dotenv()

GCP_PROJECT = os.getenv("GCP_PROJECT")
GCS_BUCKET = os.getenv("GCS_BUCKET")
DOCUMENT_AI_PROCESSOR_ID = os.getenv("DOCUMENT_AI_PROCESSOR_ID")

