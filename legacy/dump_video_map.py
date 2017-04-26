import csv
import sys

import youtube_tools

import blogspot_tools
import parser
import pickle
import datetime

import argparse

def fill_map(blogId, apikey ):
    blogmap = {}
    for blog_post in blogspot_tools.iterate_blog_posts(blogId, apikey):
        for id, title, videoId in blogspot_tools.iterate_title_and_videos(blog_post, apikey):
            blogmap[id] = (title, videoId, datetime.date.fromtimestamp(0))

    return blogmap


parser = argparse.ArgumentParser()

parser.add_argument('--blogId')
parser.add_argument('--apikey')
parser.add_argument('--inputfile')
parser.add_argument('--outputfile')

args = parser.parse_args()


fileoutname = args.outputfile
blogId =  args.blogId
apikey =  args.apikey

videoMap = fill_map(blogId, apikey )
with open(fileoutname, 'wb') as handle:
    pickle.dump(videoMap, handle,  protocol=pickle.HIGHEST_PROTOCOL)


