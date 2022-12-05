import csv
import json
import os
from xml.dom import NotFoundErr

import praw
from dotenv import load_dotenv

load_dotenv()

POSTS_PER_GAMING_SUBREDDIT = 10 * 2
POSTS_PER_GAME_SUBREDDIT = 5 * 2
USE_RELEVANT_SUBREDDITS = True

print("Instantiating PRAW")
# instantiate PRAW
reddit = praw.Reddit(client_id = os.getenv("CLIENT_ID"), client_secret= os.getenv("CLIENT_SECRET"), user_agent= os.getenv("USER_AGENT"))
print("PRAW instantiated")

print("Gathering Subreddits")
subreddits = []
# get subreddits from csv of subreddits sorted by relevance
with open("subreddits_by_relevance.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        subreddits.append(row[0])
subreddits.pop(0) # remove header

# Read subreddits from text files from Communities folder
# for filename in os.listdir("Communities"):
#     if filename.endswith(".txt"):
#         with open("Communities/" + filename, "r") as file:
#             communities = file.read().split(" OR ")
#             for community in communities:
#                 subreddits.append(community.replace("/r/", ""))
print("Subreddits read")

print("Gathering Keywords")
# Read search keywords from text files from Keywords folder

keywords = ""
with open("Keywords/RedditTitleKeywords.txt", "r") as file:
    keywords = file.read()


print("Gathering Posts Info")
post_data_headers = ["id", "subreddit", "title", "score", "comms_num", "created", "url"]
hot_posts = []
hot_posts_json = []
post_data = []
for subreddit in subreddits:
    print("Gathering in r/" + subreddit)
    try:
        hot_posts_search = reddit.subreddit(subreddit).search(query=keywords,limit=POSTS_PER_GAMING_SUBREDDIT, sort="top")
        for post in hot_posts_search:
            post_data.append([post.id, post.subreddit.display_name, post.title, post.score, post.num_comments, post.created_utc, post.url])
    except Exception as e:
        print ("Error reaching subreddit " + subreddit)

# post_data.sort(key=lambda x: x[3], reverse=True)

with open ("posts_info_sorted_relevance" + ".csv", "w", encoding='UTF-8') as file:
    write = csv.writer(file)
    write.writerow(post_data_headers)
    write.writerows(post_data)

print("Posts Info Gathered")

print("Gathering Posts Content")
# Get post IDs from posts_info_sorted_relevance.csv
post_ids = []
with open("posts_info_sorted_relevance.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        post_ids.append(row[0])
post_ids.pop(0) # remove header

# Get post content from post IDs
post_content = []
post_content_headers = ["subreddit", "title", "score", "url", "content"]
for post_id in post_ids:
    try:
        submission = reddit.submission(id=post_id)
        print("Getting content from post " + post_id + " from r/" + submission.subreddit.display_name)
        post_content_data = [submission.subreddit.display_name, submission.title, submission.score, submission.url, submission.selftext]
        post_content.append(post_content_data)
        print("Got post content")
    except Exception as e:
        print("Error reaching post " + post_id)

with open ("posts_content_sorted_relevance" + ".csv", "w", encoding='UTF-8') as file:
    write = csv.writer(file)
    write.writerow(post_content_headers)
    write.writerows(post_content)

print("Fetching posts")
exec(open("GetPostComments.py").read())
print("Posts fetched")