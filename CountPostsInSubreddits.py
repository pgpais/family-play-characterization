import csv
import os
import praw
import re
from dotenv import load_dotenv
from pmaw import PushshiftAPI

load_dotenv()
MIN_POST_THRESHOLD = 1000;

reddit = praw.Reddit(client_id = os.getenv("CLIENT_ID"), client_secret= os.getenv("CLIENT_SECRET"), user_agent= os.getenv("USER_AGENT"))
api = PushshiftAPI(praw=reddit)

# Read subreddits from text files from Communities folder
subreddits = []
for filename in os.listdir("Communities"):
    if filename.endswith(".txt"):
        with open("Communities/" + filename, "r") as file:
            communities = file.read().split("\n")
            for community in communities:
                subreddits.append(community.replace("/r/", ""))
print("Subreddits read", file=open('output.txt', 'a'))

# Get Keywords
keywords = []
print("Gathering Keywords", file=open('output.txt', 'a'))
with open("Keywords/RedditTitleKeywords.txt", "r") as file:
    line = file.read()
    keywords = line.split("\n")

# Get amount of posts in one subreddit
subreddits_relevance_data = []
subreddits_relevance_data_headers = ["subreddit", "relevance", "num_relevant_posts", "num_posts_total"]
for subreddit in subreddits:
    print("Gathering posts in r/" + subreddit, file=open('output.txt', 'a'))
    try:
        gen = api.search_submissions(subreddit=subreddit, mem_safe=True, sorted="desc", sort_type="score")
    except Exception as e:
        print ("Error reaching r/" + subreddit, file=open('output.txt', 'a'))
    print("Counting Posts in r/" + subreddit, file=open('output.txt', 'a'))
    post_count = 0
    relevant_post_count = 0
    for post in gen:
        post_count += 1
        for keyword in keywords:
            regex_keyword = r"\b"+keyword+r"\b"
            regex_search = re.search(regex_keyword, post["title"], flags=re.IGNORECASE)
            if regex_search is not None:
                relevant_post_count += 1
                break
    print(f'{post_count} posts found in r/{subreddit}', file=open('output.txt', 'a'))
    print(f'{relevant_post_count} posts found with keywords in r/{subreddit}', file=open('output.txt', 'a'))


    # Calculate relevance
    if post_count < MIN_POST_THRESHOLD:
        relevance = 0
    else:
        relevance = relevant_post_count/post_count
    subreddits_relevance_data.append([subreddit, relevance, relevant_post_count, post_count])

    # Sort subreddits by relevance
    subreddits_relevance_data.sort(key=lambda x: x[1], reverse=True)

    # Write data into a csv
    with open ("subreddits_by_relevance.csv", "w", encoding='UTF-8') as file:
        write = csv.writer(file)
        write.writerow(subreddits_relevance_data_headers)
        write.writerows(subreddits_relevance_data)


print("Subreddits sorted by relevance", file=open('output.txt', 'a'))

print("Fetching posts", file=open('output.txt', 'a'))
exec(open("GetPostsInfo.py").read())
print("Posts fetched", file=open('output.txt', 'a'))