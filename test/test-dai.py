from google.cloud import documentai_v1 as documentai

PROJECT_ID = "diagnovet-challenge"
LOCATION = "us"
PROCESSOR_ID = "dd617e5d2925f248"

FILE_PATH = "test/sample.pdf"  # poné cualquier PDF real
MIME_TYPE = "application/pdf"

client = documentai.DocumentProcessorServiceClient()

name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

with open(FILE_PATH, "rb") as f:
    file_content = f.read()

request = documentai.ProcessRequest(
    name=name,
    raw_document=documentai.RawDocument(
        content=file_content,
        mime_type=MIME_TYPE
    )
)

result = client.process_document(request=request)

document = result.document

print("Texto completo extraído:")
print(document.text[:1000])
