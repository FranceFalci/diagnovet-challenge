
from app.services.firestore import get_report
from app.services.storage import generate_signed_url
from app.config import GCS_BUCKET


def get_report_by_id(report_id: str) -> dict | None:
    report = get_report(report_id)

    if not report:
        return None

    signed_images = [
        generate_signed_url(GCS_BUCKET, img)
        for img in report.get("images", [])
    ]

    return {
        "report_id": report_id,
        "data": report.get("data"),
        "images": signed_images,
    }
