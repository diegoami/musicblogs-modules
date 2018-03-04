import csv
import sys
import os
from . import youtube_tools

from . import blogspot_tools
import parser
import pickle
import datetime

import argparse

def fill_map(blogId, apikey, blogMap, debug=False ):
    newBlogMap = {}
    for postList in blogspot_tools.iterate_blog_posts(blogId, apikey):

        for blogPost in blogspot_tools.iterate_title_and_videos(postList, apikey):

            if blogPost.postId not in blogMap or blogMap.postId[1] != blogPost.videoId:
                debug and print("Updating "+blogPost.postId+" to "+blogPost.videoId)
                newBlogMap[blogPost.postId] = (blogPost.title, blogPost.videoId, datetime.date.fromtimestamp(0))
            else:
                debug and print("Ignoring " + blogPost.postId + " and " + blogPost.videoId)
                newBlogMap[blogPost.postId] = blogMap[blogPost.postId]
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


