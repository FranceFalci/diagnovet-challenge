# Diagnovet Challenge – Veterinary Diagnostic API

## Overview

This project implements a **production-ready backend API** for processing veterinary diagnostic reports. The service allows uploading PDF medical reports, extracting their content via OCR, cleaning and normalizing the text, and generating structured diagnostic outputs. The system is designed with cloud-native principles and deployed on **Google Cloud Platform**.

The repository demonstrates practical skills in **backend development, containerization, cloud deployment, authentication, and ML service integration**.

---

## Features

* REST API built with **FastAPI**
* Secure endpoints using **Bearer Token authentication**
* PDF upload and processing
* OCR-based text extraction from medical reports
* Text cleaning and normalization for downstream processing
* Containerized with **Docker**
* Deployed on **Google Cloud Run**
* Artifact storage using **Google Artifact Registry**
* Cloud authentication via **Application Default Credentials (ADC)**

---

## Tech Stack

* **Python**
* **FastAPI** – Web framework for building APIs
* **Uvicorn** – ASGI server for FastAPI
* **Docker** – Containerization of the application
* **Google Cloud Run** – Serverless container execution
* **Google Cloud Storage** – Storage for uploaded PDFs and generated reports
* **Document AI** – OCR and structured text extraction from PDF documents
* **Firestore** – NoSQL database for storing report metadata and extracted results
* **Vertex AI** – Managed platform for running and integrating machine learning models


---

## Project Structure

```
app/
 ├── api/
 │   └── routes.py          # API endpoints
 ├── auth/
 │   └── security.py        # Token verification logic
 ├── services/
 │   └── 
 ├── use_cases/
 │   ├── create_report.py   # Core business logic
 │   └── get_report.py
 ├── utils/
 │   └── text_cleaning.py   
 └── main.py                # Application entrypoint
Dockerfile
requirements.txt
```

---

## API Endpoints

### `POST /reports`

Uploads a veterinary diagnostic report in PDF format.

* **Authentication**: Bearer Token (Authorization header)
* **Request**: `multipart/form-data`

  * `file`: PDF file
* **Response**: JSON with processed report data

### `GET /reports/{report_id}`

Retrieves a previously generated report.

---

## Authentication

All protected endpoints require a Bearer Token:

```
Authorization: Bearer <TOKEN>
```

The token is validated server-side using a custom dependency.

---

## Running Locally

### 1. Clone the repository

```
git clone https://github.com/FranceFalci/diagnovet-challenge.git
cd diagnovet-challenge
```

### 2. Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set environment variables

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export API_TOKEN=your_token_here
```

### 5. Run the application

```
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Running with Docker

### Build the image

```
docker build -t vet-api .
```

### Run the container

```
docker run -p 8000:8000 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/credentials.json \
  -e API_TOKEN=your_token_here \
  vet-api
```

---

## Deployment on Google Cloud Run

The application is deployed using:

* **Artifact Registry** for container images
* **Cloud Run** for serverless execution

High-level steps:

1. Build Docker image in Cloud Shell
2. Push image to Artifact Registry
3. Deploy service to Cloud Run
4. Configure environment variables and service account

Cloud Run provides:

* Automatic scaling
* HTTPS endpoint
* Managed infrastructure

---

## How to Test the API

### Using Swagger

1. Open `/docs`
2. Click **Authorize**
3. Enter:

```
Bearer <TOKEN>
```

4. Use `POST /reports` and upload a PDF

### Using Postman

* Method: `POST`
* URL: `/reports`
* Headers:

  * `Authorization: Bearer <TOKEN>`
* Body:

  * `form-data`

    * key: `file` (type: File)
    * value: PDF file

---

## Notes

* Tokens are intentionally **not stored in the repository** for security reasons.
* Service accounts and credentials must be configured via environment variables.



## Author

**Francesca Falci**
Backend / Cloud / ML Engineer
