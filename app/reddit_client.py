from typing import List


def fetch_posts(topic: str) -> List[str]:
    """
    Placeholder for Reddit API.
    For now returns dummy posts for the topic.
    """
    dummy_posts = {
        "Climate Change": [
            "We must act now.",
            "This is exaggerated.",
            "Uncertain evidence."
        ],
        "AI Regulation": [
            "We need guardrails.",
            "Overregulation stifles progress.",
            "Balance is required."
        ],
        "Universal Basic Income": [
            "It reduces poverty.",
            "Too expensive.",
            "Still experimental."
        ]
    }
    return dummy_posts.get(topic, ["No relevant posts found."])
