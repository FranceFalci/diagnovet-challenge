from fastapi import APIRouter, UploadFile, File, Depends
from app.auth.security import verify_token

router = APIRouter()

@router.post("/reports")
async def upload_report(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    return {"message": "PDF received"}

@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    return {"report_id": report_id}
