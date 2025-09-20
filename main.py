from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from app.agent_logic import analyze_topic
import os
import jwt
# from dotenv import load_dotenv # for localhost

# # for localhost
# load_dotenv()
# JWT_SECRET = os.getenv("JWT_SECRET")

app = FastAPI()

# CORS setup
origins = [
    "https://ioa-sa-polarization-mapper.streamlit.app",  # deployed frontend
    "http://localhost:8501"  # local frontend testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TopicRequest(BaseModel):
    topic: str


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


def verify_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/analyze")
def analyze(request: TopicRequest, authorization: str = Header(None)) -> Dict[str, Any]:
    if not authorization:
        raise HTTPException(
            status_code=401, detail="Missing Authorization header")

    try:
        token_type, token = authorization.split()
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format")

    # Verify JWT
    verify_jwt(token)

    return analyze_topic(request.topic)
