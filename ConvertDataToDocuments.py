import csv
import os
from xml.dom import NotFoundErr

with open('comments_data.csv', mode ='r', encoding='UTF-8') as file:
    # reading the CSV file
    data = csv.reader(file)
    documents_path = "./Documents/"

    post_count = 0
    line_count = 0
    for row in data:
        if(len(row) <= 0):
            continue
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        else:
            with open(documents_path + row[1] + '-' + row[0] + ".txt", 'w+', encoding="utf-8") as file:
                file.write("Title\n")
                file.write(row[3]+"\n")
                file.write("\n")
                file.write("Post\n")
                file.write(row[4]+"\n")
                file.write("\n")
                file.write("Comment\n")
                file.write(row[5]+"\n")
        line_count+=1   