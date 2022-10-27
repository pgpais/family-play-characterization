import csv
import os
from xml.dom import NotFoundErr
import praw
from dotenv import load_dotenv
import json
load_dotenv()

# instantiate PRAW
reddit = praw.Reddit(client_id = os.getenv("CLIENT_ID"), client_secret= os.getenv("CLIENT_SECRET"), user_agent= os.getenv("USER_AGENT"))
print("PRAW instantiated")

# Read subreddits from text files from Communities folder
subreddits = []
for filename in os.listdir("Communities"):
    if filename.endswith(".txt"):
        with open("Communities/" + filename, "r") as file:
            communities = file.read().split(" OR ")
            for community in communities:
                subreddits.append(community.replace("/r/", ""))
print("Subreddits read")

print("Gathering Information on Subreddits")
subreddit_info_headers = ["name", "description", "subscribers"]
subreddit_info = []
for subreddit_name in subreddits:
    print("Gathering Information on r/" + subreddit_name)
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit_info.append([subreddit.display_name, subreddit.description, subreddit.subscribers])
    except Exception as e:
        print ("Error reaching subreddit " + subreddit_name)

subreddit_info.sort(key=lambda x: x[2], reverse=True)

with open ("subreddit_info.csv", "w", encoding='UTF-8') as file:
    write = csv.writer(file)
    write.writerow(subreddit_info_headers)
    write.writerows(subreddit_info)
print("Subreddit Information Gathered")