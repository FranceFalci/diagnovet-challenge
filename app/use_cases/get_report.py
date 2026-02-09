import logging
from app.services.firestore import get_report
from app.services.storage import generate_signed_url
from app.config import GCS_BUCKET

logger = logging.getLogger("diagnovet.get_report")

def get_report_by_id(report_id: str) -> dict | None:
    try:
        logger.info(f"🔍 Buscando reporte {report_id} en Firestore...")
        try:
            report = get_report(report_id)
        except Exception as e:
            logger.error(f" Error de conexión con Firestore para ID {report_id}: {str(e)}")
            raise e

        if not report:
            logger.warning(f" Reporte {report_id} no encontrado.")
            return None

        raw_images = report.get("images", [])
        signed_images = []
        
        logger.info(f"🖼️ Firmando {len(raw_images)} imágenes...")

        for img_path in raw_images:
            try:
                signed_url = generate_signed_url(GCS_BUCKET, img_path)
                signed_images.append(signed_url)
            except Exception as e:
                logger.error(f"❌ Error firmando imagen '{img_path}': {str(e)}")
                continue 

        logger.info(f"✅ Reporte {report_id} recuperado con éxito.")
        return {
            "report_id": report_id,
            "data": report.get("data"),
            "images": signed_images, 
        }

    except Exception as e:
        logger.critical(f"🔥 Error crítico no manejado en get_report_by_id: {str(e)}")
        raise e