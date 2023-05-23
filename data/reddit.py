import snscrape.modules.reddit as snreddit
import pandas as pd

from ..utils.helpers import random_id

def get_reddit_posts(query: str, limit: int = 100, save_df: bool = False) -> pd.DataFrame:
    posts = []
    max_length = 500
    for i, post in enumerate(snreddit.RedditSearchScraper(query).get_items()):
        if i >= limit:
            break
        is_comment = isinstance(post, snreddit.Comment)
        if is_comment and len(post.body) < max_length:
            posts.append([post.date, post.subreddit, post.body, is_comment, post.parentId, post.url])
        elif not is_comment and len(post.title) < max_length:
            posts.append([post.date, post.subreddit, post.title, is_comment, post.id, post.url])
        else:
            continue

    df = pd.DataFrame(posts, columns=["Date", "Subreddit", "Title/Body", "Is Comment", "ID/Parent ID", "URL"])
    if save_df:
        df.to_csv(f"reddit-{query.replace(' ', '-')}-{random_id()}.csv", index=False)
    return df

# print(get_reddit_posts("oil industry", limit=1000, save_df=True))