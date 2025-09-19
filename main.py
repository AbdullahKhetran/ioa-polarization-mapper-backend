from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from app.agent_logic import analyze_topic


app = FastAPI()


class TopicRequest(BaseModel):
    topic: str


@app.post("/analyze")
def analyze(request: TopicRequest) -> Dict[str, Any]:
    return analyze_topic(request.topic)
