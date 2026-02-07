from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

doc_ref = db.collection("reports").document("test-report-1")

data = {
    "patient": "Firulais",
    "diagnosis": "Hip dysplasia",
    "created_at": datetime.utcnow(),
    "status": "processed"
}

doc_ref.set(data)

print("Documento guardado")

doc = doc_ref.get()
print("Documento leído:")
print(doc.to_dict())
