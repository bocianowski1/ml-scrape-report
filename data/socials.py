import snscrape.modules.twitter as sntwitter
import snscrape.modules.reddit as snreddit
import random
import pandas as pd
# snscrape-0.6.2.20230320

def random_id(a: int = 1000, b: int = 9999) -> int:
    return random.randint(a, b)

# TWITTER

def advanced_query(user: str = None, since: str = "2021-01-01", until: str = None) -> str:
    if user is None:
        return f"since:{since} until:{until}"
    else:
        return f"from:{user} since:{since} until:{until}"

def get_tweets(query: str, limit: int = 100, save_df: bool = False) -> pd.DataFrame:
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        print(vars(tweet), type(tweet), tweet)
        tweets.append([tweet.created, tweet.username, tweet.description])
    df = pd.DataFrame(tweets, columns=["Date", "Username", "Content"])
    if save_df:
        df.to_csv(f"twitter-{query.replace(' ', '-')}-{random_id()}.csv", index=False)
    return df

# REDDIT

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

if __name__ == "__main__":
    tweets = get_tweets("oil industry", limit=1000, save_df=True)
    print(tweets)