import csv


print("Collect Comments")
comments_data = []
with open('comments_data.csv', mode ='r') as file:
    # reading the CSV file
    csvComments = csv.reader(file)

    post_count = 0
    line_count = 0
    for csv_comment in csvComments:
        if(len(csv_comment) <= 0):
            continue
        else:
            comments_data.append(csv_comment)
print("Comments Collected")

print("Sorting Comments")
comments_data.sort(key=lambda x: x[4], reverse=True)
print("Comments Sorted")

print("Saving Comments")
with open('comments_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comment_data in comments_data:
        writer.writerow(comment_data)