from fastapi import Header, HTTPException
import os

API_TOKEN = os.getenv("API_TOKEN")

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
