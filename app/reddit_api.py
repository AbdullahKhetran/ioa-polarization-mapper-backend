import praw
import os
from dotenv import load_dotenv

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def fetch_posts(topic, limit=10):

    results = []

    for submission in reddit.subreddit("all").search(topic, limit=limit, sort="relevance"):
        submission.comments.replace_more(limit=0)  # flatten "MoreComments"
        comments = [c.body.replace("\n", " ")
                    for c in submission.comments[:10]]

        results.append({
            "id": submission.id,
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "permalink": f"https://www.reddit.com{submission.permalink}",
            "description": submission.selftext[:500] or "[No description]",
            "comments": comments
        })

    return results
