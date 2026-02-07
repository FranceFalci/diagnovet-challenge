from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Ultrasound PDF API")

app.include_router(router)
