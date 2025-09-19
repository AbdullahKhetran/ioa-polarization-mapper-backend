from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from app.agent_logic import analyze_topic


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


@app.post("/analyze")
def analyze(request: TopicRequest) -> Dict[str, Any]:
    return analyze_topic(request.topic)
