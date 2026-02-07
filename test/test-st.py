from google.cloud import storage

BUCKET_NAME = "diagnovet-reports-bucket"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

blob = bucket.blob("test/hello.txt")
blob.upload_from_string("hola gcp")

print("Archivo subido correctamente")
