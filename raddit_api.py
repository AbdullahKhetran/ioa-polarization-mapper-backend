import praw

# 🔑 App credentials (use env vars later for security!)
reddit = praw.Reddit(
    client_id="your_id",
    client_secret="you_key",
    user_agent="name_agent"
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
