from pydantic import BaseModel, Field
from typing import Optional, List

class AIReportExtraction(BaseModel):
    patient: Optional[str]
    owner: Optional[str]
    veterinarian: Optional[str]
    diagnosis: Optional[str]
    recommendations: Optional[List[str]]

class ReportData(AIReportExtraction): 
    raw_text: str  
    created_at: Optional[str] = None