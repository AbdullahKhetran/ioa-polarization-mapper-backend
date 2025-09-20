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

query = "climate change"

print(f"\n🔎 Searching for: {query}\n")

for idx, submission in enumerate(
    reddit.subreddit("all").search(query, limit=10, sort="relevance"), start=1
):
    print(f"📌 Post {idx}")
    print(f"Title      : {submission.title}")
    print(f"Score      : {submission.score}")
    print(f"URL        : {submission.url}")
    print(f"Permalink  : https://www.reddit.com{submission.permalink}")
    print(f"Description: {submission.selftext[:500] or '[No description]'}")
    print("\n💬 Top 10 Comments:")

    # Load comments (replace MoreComments with actual comments)
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()

    for i, comment in enumerate(comments[:10], start=1):
        text = comment.body.replace("\n", " ")
        print(f"  {i}. {text[:200]}")  # truncate long comments for readability

    print("\n" + "=" * 120 + "\n")
