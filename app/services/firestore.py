from google.cloud import firestore

db = firestore.Client()

def save_report(report_id: str, data: dict):
    db.collection("reports").document(report_id).set(data)

def get_report(report_id: str):
    doc = db.collection("reports").document(report_id).get()
    return doc.to_dict()
