from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

def verify_token(authorization: str = Header(...)):
    print("DEBUG TOKEN:", API_TOKEN)
    print("DEBUG AUTHORIZATION:", authorization)
    if authorization != f"Bearer {API_TOKEN}":
        print("DEBUG UNAUTHORIZED")
        raise HTTPException(status_code=401, detail="Unauthorized")
