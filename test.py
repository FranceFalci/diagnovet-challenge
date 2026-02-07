import os
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET = os.getenv("GCS_BUCKET")

print("DEBUG BUCKET:", GCS_BUCKET)
