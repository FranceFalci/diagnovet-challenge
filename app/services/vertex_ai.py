import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
from app.domain.report_schema import AIReportExtraction

def extract_structured_data(project_id: str, location: str, text: str) -> dict:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-2.5-flash-lite")
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "patient": {
                "type": "STRING",
                "nullable": True
            },
            "owner": {
                "type": "STRING",
                "nullable": True
            },
            "veterinarian": {
                "type": "STRING",
                "nullable": True
            },
            "diagnosis": {
                "type": "STRING",
                "nullable": True
            },
            "recommendations": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                },
                "nullable": True
            }
        },
        "required": ["patient", "owner", "veterinarian", "diagnosis", "recommendations"]
    }
    # -----------------------

    prompt = f"""
    You are a veterinary AI assistant. Extract clinical data from the following raw OCR text.
ONLY extract data that is explicitly present in the text.
Do NOT invent or guess anything. If a field is missing, return null (for strings) or an empty array (for lists).
Do NOT include any metadata or noise in your response.


    Map the following Spanish terms to the English JSON keys:
    - "Paciente" / "Mascota"  -> patient
    - "Propietario" / "Dueño" / "Dueña" / "Tutor" -> owner
    - "Referido" / "Referido por" / "Profesional" /  "Derivante"  / "Veterinario" / "Médico Veterinario" -> veterinarian
    - "Conclusion" / "Diagnostico" -> diagnosis
    
    Raw Text:
    {text}
    """

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0
        )
    )

    return json.loads(response.text)