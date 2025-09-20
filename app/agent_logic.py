import os
import requests
from app.reddit_api import fetch_posts
from dotenv import load_dotenv
import json

load_dotenv()
AIML_API_KEY = os.getenv("AIML_API_KEY")


def build_prompt(topic: str, posts) -> str:
    """
    Build the AI prompt dynamically using the topic and list of posts
    """
    prompt = f"""
    You are a polarization analysis agent. 

    Task:
    1. You are given a list of Reddit posts on a specific topic.
    2. You must choose ONE method to calculate the polarization score from the following predefined methods:
    - Balance Metric: Measures how evenly opinions are split between opposing views.
    - Entropy Score: Uses information entropy to measure opinion diversity.
    - Sentiment Variance: Calculates the variance of sentiment scores across posts.

    3. After selecting the method, calculate a polarization score between 0.0 and 1.0:
    - 0.0 means no polarization (everyone agrees)
    - 1.0 means maximum polarization (opinions are evenly split in extremes)

    Input:
    - Topic: {topic}
    - Posts:
    """
    # Add each post dynamically
    for post in posts:
        prompt += f'  - (id={post["id"]}) "{post["title"]}"\n'

    # Add instructions for AI to respond in JSON
    prompt += """
    Instructions:
    1. Pick the most appropriate method for these posts.
    2. Explain in 1-2 sentences why you picked this method.
    3. Calculate the polarization score based on the selected method.
    4. Include up to 3 example post IDs that influenced your decision.
    5. Output strictly in the following JSON format:

    {
    "selected_method": "<method_name>",
    "reason": "<short_reason_for_method_choice>",
    "polarization_score": <score_between_0_and_1>,
    "example_post_ids": ["<id1>", "<id2>", "<id3>"]
    }

    Important:
    - Only respond with the JSON (no extra text).
    - The score must be a float between 0.0 and 1.0.
    """
    return prompt


def call_ai_service(prompt):
    """
    Calls the external AI/ML API to process posts.
    """
    if not AIML_API_KEY:
        raise ValueError("AIML_API_KEY not set in environment")

    url = "https://api.aimlapi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    # print("data from ai model", response.json())
    return response.json()


def extract_ai_result(full_response):
    """
    Extracts the relevant data from the full AI/ML API response.

    Returns a dictionary with:
    - selected_method
    - reason
    - polarization_score
    - example posts id
    """
    try:
        # Navigate to the content string in the response
        content_str = full_response["choices"][0]["message"]["content"]
        # Convert JSON string to dict
        parsed = json.loads(content_str)
        # Ensure all required keys exist
        result = {
            "selected_method": parsed.get("selected_method", "unknown"),
            "reason": parsed.get("reason", ""),
            "polarization_score": parsed.get("polarization_score", 0.0),
            "example_post_ids": parsed.get("example_post_ids", [])
        }
    except (KeyError, IndexError, json.JSONDecodeError):
        # Fallback if response format is unexpected
        result = {
            "selected_method": "unknown",
            "reason": "Could not parse AI response",
            "polarization_score": 0.0,
            "example_post_ids": []
        }

    return result


def analyze_topic(topic: str):

    reddit_data = fetch_posts(topic)

    if not reddit_data:
        return {"topic": topic, "polarization_score": 0.0}

    selected_reddit_data = []  # send only id and titles of post
    for post in reddit_data:
        id = post.get("id")
        title = post.get("title", "[No title]")
        selected_reddit_data.append({"id": id, "title": title})

    prompt = build_prompt(topic, selected_reddit_data)

    ai_response = call_ai_service(prompt)  # ai full response

    data = extract_ai_result(ai_response)  # json of required fields

    return data
