import csv
import sys

import youtube_tools

from legacy import blogspot_tools


def print_videos_in_blog(blog_id, apikey, fileout):
    print("Now parsing blog "+blog_id+" with key "+apikey)
    for blog_post in blogspot_tools.iterate_blog_posts(blog_id, apikey):
        for title, video in blogspot_tools.iterate_title_and_videos(blog_post, apikey):
            if title is not None:
                if video is not None:
                    validLink = youtube_tools.verify_link(title, video, apikey)
                    fileout.write(title+","+ video+","+ str(validLink) +'\n')
                else:
                    fileout.write(title + ",NotFound,False\n")


if len(sys.argv) < 2:
    print("Usage : python list_youtube_videos.py <blogsfile.txt>")
    print("Each row must be in the form blogid,apikey")
    sys.exit(0)
else:
    filename= sys.argv[1]

fileoutname = 'videolist.txt'
if len(sys.argv) >= 3:
    fileoutname = sys.argv[2]
fileout =  open(fileoutname, 'w',encoding='utf-8')




with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            print("Each row must be in the form blogid,apikey")
            print("Skipping....")
        else:

            print_videos_in_blog(row[0], row[1], fileout)