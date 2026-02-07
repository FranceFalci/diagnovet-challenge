import uuid
from app.services.storage import upload_pdf, upload_image
from app.services.document_ai import process_document
from app.utils.pdf_images import extract_images
from app.utils.clean_text import clean_text
from app.services.firestore import save_report
from app.services.vertex_ai import extract_structured_data
from app.domain.report_schema import ReportData
from app.config import (
    GCS_BUCKET,
    GCP_PROJECT,
    DOCUMENT_AI_PROCESSOR_ID,
)

def create_report(file_bytes: bytes, filename: str) -> str:
    report_id = str(uuid.uuid4())

    # 1. PDF a GCS
    pdf_path = upload_pdf(
        file_bytes=file_bytes,
        filename=filename,
        bucket_name=GCS_BUCKET,
        report_id=report_id,
    )

    # 2. Imágenes (ultrasonidos)
    images = extract_images(file_bytes)
    image_paths = [
        upload_image(img, GCS_BUCKET, report_id, idx)
        for idx, img in enumerate(images)
    ]

    # 3. OCR + layout
    document = process_document(
        project_id=GCP_PROJECT,
        location="us",
        processor_id=DOCUMENT_AI_PROCESSOR_ID,
        file_bytes=file_bytes,
    )

    full_text = clean_text(document.text)

    # 4. Vertex AI (estructuración)
    structured = extract_structured_data(
        project_id=GCP_PROJECT,
        location="us-central1",
        text=full_text,
    )

    report_data = ReportData(
        **structured,
        raw_text=full_text
    )

    # 5. Persistencia
    save_report(report_id, {
        "pdf_path": pdf_path,
        "images": image_paths,
        "data": report_data.dict(),
    })

    return report_id
