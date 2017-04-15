import csv
import requests
import json
import re
import sys
import blogspot_tools 

        
if len(sys.argv) < 2:
    print("Usage : python list_youtube_videos.py <blogsfile.txt>")
    print("Each row must be in the form blogid,apikey")
    sys.exit(0)
else:
    filename= sys.argv[1]
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            print("Each row must be in the form blogid,apikey")
            print("Skipping....")
        else:
            print("Now parging blog "+row[0]+" with key "+row[1])
            for blog_post in blogspot_tools.iterate_blog_posts(row[0],row[1]):
                print(blog_post)