import os
import praw
from dotenv import load_dotenv
import pandas as pd
from pmaw import PushshiftAPI
load_dotenv()

# instantiate PRAW
reddit = praw.Reddit(client_id = os.getenv("CLIENT_ID"), client_secret= os.getenv("CLIENT_SECRET"), user_agent= os.getenv("USER_AGENT"))
print("PRAW instantiated")

# instantiate PMAW
api = PushshiftAPI(praw=reddit)
print("PMAW instantiated")

print("PRAW TOP POSTS IN r/gaming")
hot_posts_praw = reddit.subreddit("gaming").top(limit=5)
for post in hot_posts_praw:
    print(post.title)

print("PMAW TOP POSTS IN r/gaming")
hot_posts_pmaw = api.search_submissions(subreddit='gaming', limit=5, sort_type='score', sort='desc')
print(f'Number of posts: {len(hot_posts_pmaw)}')
hot_posts_pmaw_list = [p for p in hot_posts_pmaw]
for post in hot_posts_pmaw_list:
    print(post.title)