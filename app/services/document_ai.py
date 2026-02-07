# app/services/document_ai.py
from google.cloud import documentai_v1 as documentai

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_bytes: bytes
):
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    document = {"content": file_bytes, "mime_type": "application/pdf"}
    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)
    return result.document
