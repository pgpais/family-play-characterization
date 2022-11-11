import csv
import os
import praw
from dotenv import load_dotenv
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
keywords_titles =["general_keywords", "title_keyword", "title_keywords_no_kinship"]
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


print("Counting Posts")
post_data_headers =["subreddit", "num_posts"]

# Count posts
for keywords_title in keywords_titles:
    keywords = keywords_list[keywords_title]
    hot_posts = []
    hot_posts_json = []
    post_data = []

    # Count posts in each subreddit
    for subreddit in subreddits:
        title_keyword_count = 0
        print("Counting in r/" + subreddit)
        try:
            hot_posts_search = reddit.subreddit(subreddit).search(query=keywords, limit=None, sort="top")
            for post in hot_posts_search:
                title_keyword_count += 1
        except Exception as e:
            title_keyword_count = -1
            keyword_count = -1
            print ("Error reaching subreddit " + subreddit)
        post_data.append([subreddit, title_keyword_count])

    # Sort data by number of posts (so we don't have to sort it later)
    post_data.sort(key=lambda x: x[1], reverse=True)

    # Write data into a csv
    with open ("subreddit_info_" + keywords_title + ".csv", "w", encoding='UTF-8') as file:
        write = csv.writer(file)
        write.writerow(post_data_headers)
        write.writerows(post_data)

    print("Count " + keywords_title + " complete")
print("Posts Counted")
