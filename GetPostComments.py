import csv
import os
from xml.dom import NotFoundErr
import praw
from dotenv import load_dotenv
import json
load_dotenv() # Load environment variables from .env file

# Search Variables
max_comments = 1 # How many top-level comments per post
max_posts = -1 # How many posts to search

# instantiate PRAW
reddit = praw.Reddit(client_id = os.getenv("CLIENT_ID"), client_secret= os.getenv("CLIENT_SECRET"), user_agent= os.getenv("USER_AGENT"))
print("PRAW instantiated", file=open('output.txt', 'a'))

# Get subreddit IDs
post_ids = []
print("Gathering Post IDs", file=open('output.txt', 'a'))
with open('included_posts.csv', mode ='r', encoding='UTF-8') as file:
    # reading the CSV file
    csvPosts = csv.reader(file)

    post_count = 0
    line_count = 0
    for comment_data in csvPosts:
        if(max_posts > 0 and post_count >= max_posts):
            break
        if(len(comment_data) <= 0):
            continue
        if line_count == 0:
            print(f'Column names are {", ".join(comment_data)}', file=open('output.txt', 'a'))
        else:
            post_ids.append(comment_data[0])
            post_count += 1

        line_count += 1
print("Post IDs Gathered", file=open('output.txt', 'a'))


print("Gathering Comments", file=open('output.txt', 'a'))
comment_csv_headers = ["subreddit","post_id","comment_id", "post_title", "post_body",  "comment_body", "comment_score"]
comments_data = []
comments_data.append(comment_csv_headers)

for post_id in post_ids:
    print("Gathering Comments for Post: " + post_id, file=open('output.txt', 'a'))
    submission = reddit.submission(id=post_id)
    submission.comment_sort = 'top'
    submission.comments.replace_more(limit=None)
    comments = submission.comments
    print("Comments Gathered", file=open('output.txt', 'a'))

    print("Checking Comments for post: " + post_id, file=open('output.txt', 'a'))
    comment_count = 0
    for comment in comments:
        if(max_comments > 0 and comment_count >= max_comments):
            break
        comment_data = [submission.subreddit.display_name, post_id, comment.id, submission.title, submission.selftext, comment.body, comment.score]
        comments_data.append(comment_data)
        comment_count += 1
        print("Comment Found for post "+ post_id +": " + comment.id, file=open('output.txt', 'a'))

with open('comments_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comment_data in comments_data:
        writer.writerow(comment_data)
print("Comments Gathered", file=open('output.txt', 'a'))
