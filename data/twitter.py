import snscrape.modules.twitter as sntwitter
import pandas as pd
# snscrape-0.6.2.20230320

from ..utils.helpers import random_id

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

# tweets = get_tweets("oil industry", limit=1000, save_df=True)