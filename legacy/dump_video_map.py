import csv
import sys
import os
import youtube_tools

import blogspot_tools
import parser
import pickle
import datetime

import argparse

def fill_map(blogId, apikey, blogMap, debug=False ):
    newBlogMap = {}
    for blog_post in blogspot_tools.iterate_blog_posts(blogId, apikey):
        for id, title, videoId in blogspot_tools.iterate_title_and_videos(blog_post, apikey):
            if id not in blogMap or blogMap[id][1] != videoId:
                debug and print("Updating "+id+" to "+videoId)
                newBlogMap[id] = (title, videoId, datetime.date.fromtimestamp(0))
            else:
                debug and print("Ignoring " + id + " and " + videoId)
                newBlogMap[id] = blogMap[id]
    return newBlogMap


parser = argparse.ArgumentParser()

parser.add_argument('--blogId')
parser.add_argument('--apikey')
parser.add_argument('--outputfile')
parser.add_argument('--debug')

args = parser.parse_args()
debug = True if args.debug else False
initialMap = {}
if os.path.isfile(args.outputfile):
    with open(args.outputfile, 'rb') as handle:
        initialMap = pickle.load(handle)


videoMap = fill_map( args.blogId, args.apikey, initialMap ,debug=args.debug )
with open(args.outputfile, 'wb') as handle:
    pickle.dump(videoMap, handle,  protocol=pickle.HIGHEST_PROTOCOL)


