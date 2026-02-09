import uuid
import logging
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("diagnovet.create_report")

def create_report(file_bytes: bytes, filename: str) -> str:
    report_id = str(uuid.uuid4())
    
    logger.info(f"[START] Iniciando procesamiento. Report ID: {report_id} | Archivo: {filename}")

    try:
        images = extract_images(file_bytes)

        image_paths = []
        for idx, img in enumerate(images):
            path = upload_image(img, GCS_BUCKET, report_id, idx)
            image_paths.append(path)
        
        document = process_document(
            project_id=GCP_PROJECT,
            location="us",
            processor_id=DOCUMENT_AI_PROCESSOR_ID,
            file_bytes=file_bytes,
        )

        full_text = clean_text(document.text)

        structured = extract_structured_data(
            project_id=GCP_PROJECT,
            location="us-central1",
            text=full_text,
        )

        report_data = ReportData(
            **structured,
            raw_text=full_text
        )

        save_report(report_id, {
            "images": image_paths,
            "data": report_data.dict(),
        })

        logger.info(f"[END] Reporte {report_id} creado exitosamente.")
        return report_id

    except Exception as e:
        logger.error(f"[ERROR] Falló el proceso para el reporte {report_id}.")
        logger.error(f"Detalle del error: {str(e)}")
        raise e