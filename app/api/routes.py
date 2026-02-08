from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.auth.security import verify_token
from app.use_cases.create_report import create_report
from app.use_cases.get_report import get_report_by_id

router = APIRouter()

@router.post("/reports")
async def upload_report(
    file: UploadFile = File(...),
        token: str = Depends(verify_token)
):
    # print("DEBUG file.filename:", file.filename)
    # print("DEBUG token:", token)
    pdf_bytes = await file.read()
    result = create_report(file_bytes=pdf_bytes, filename=file.filename)
    return result

@router.get("/reports/{report_id}")
async def get_report_endpoint(report_id: str):
    result = get_report_by_id(report_id)

    if not result:
        raise HTTPException(status_code=404, detail="Report not found")

    return result
