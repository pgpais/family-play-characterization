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

print("Gathering Keywords")
keywords_titles =["general_keywords", "title_keywords", "title_keywords_no_kinship"]
keywords_list = {}
# Read search keywords from text files from Keywords folder
keywords_list["general_keywords"] = ""
with open("Keywords/RedditKeywords.txt", "r") as file:
    keywords_list["general_keywords"] = file.read()

keywords_list["title_keywords"] = ""
with open("Keywords/RedditTitleKeywords.txt", "r") as file:
    keywords_list["title_keywords"] = file.read()

keywords_list["title_keywords_no_kinship"] = ""
with open("Keywords/RedditTitleKeywordsNoKinship.txt", "r") as file:
    keywords_list["title_keywords_no_kinship"] = file.read()
print("Keywords read")


print("Gathering Posts")
post_data_headers = ["id", "subreddit", "title", "score", "comms_num", "created", "url"]
for keywords_title in keywords_titles:
    keywords = keywords_list[keywords_title]
    hot_posts = []
    hot_posts_json = []
    post_data = []
    for subreddit in subreddits:
        print("Searching in r/" + subreddit)
        try:
            hot_posts_search = reddit.subreddit(subreddit).search(query=keywords,limit=5, sort="top")
            for post in hot_posts_search:
                if(post.is_self):
                    # print(post.subreddit.display_name + " POST: " + post.title)
                    hot_posts.append(post)
                    post_data.append([post.id, post.subreddit.display_name, post.title, post.score, post.num_comments, post.created_utc, post.url])
        except Exception as e:
            print ("Error reaching subreddit " + subreddit)

    with open ("hot_posts_data_" + keywords_title + ".csv", "w", encoding='UTF-8') as file:
        write = csv.writer(file)
        write.writerow(post_data_headers)
        write.writerows(post_data)

    hot_posts_json = json.dumps(hot_posts_json, indent=4)
    json_file = open(keywords_title + "_hot_posts.json", "w")
    json_file.write(hot_posts_json)
    json_file.close()
    print("Search " + keywords_title + " complete")
print("Posts Gathered")
