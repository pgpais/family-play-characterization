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




print("Gathering Post IDs")
post_ids = []
with open('posts_info_title_keywords.csv', mode ='r') as file:
    # reading the CSV file
    csvPosts = csv.reader(file)

    # Get first 5 lines of csvPosts
    line_count = 0
    for row in csvPosts:
        if(len(row) <= 0):
            continue
        if line_count > 5:
            break
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        else:
            post_ids.append(row[0])

        line_count += 1
print("Post IDs Gathered")


print("Gathering Posts")
for post_id in post_ids:
    submission = reddit.submission(id=post_id)
    submission.comment_sort = "top"
    comments = submission.comments
    print(comments[0].body)
print("Posts Gathered")
