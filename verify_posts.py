
import argparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
import sys
from legacy import youtube_tools

import argparse
import codecs


from legacy.blogspot_tools import iterate_blog_posts, iterate_title_and_videos, BlogPost
import yaml

def verify_blog_collection(posts_collection, blogId, apiKey, data=None):
    for postId, blogPost in data.items():
        if not blogPost:
            continue

        if not hasattr(blogPost, "videoId"):
            continue

        if not blogPost.videoId:
            continue


        validLink = youtube_tools.verify_link(blogPost.title, blogPost.videoId, apiKey)
        if not validLink:
            print('=========================================================')
            print(u'MISSING VIDEO {} IN POST {} : {}'.format(blogPost.videoId, postId, blogPost.title))
            print('=========================================================')
        else:
            print(u'Successfully processed videos {} in post {} : {}'.format(blogPost.videoId, postId, blogPost.title))



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')
    api_key = os.getenv("BLOG-API-KEY")
    mongo_connection = os.getenv("mongo_connection")

    args = parser.parse_args()
    api_key = os.getenv("BLOG-API-KEY")
    mongo_connection = os.getenv("mongo_connection")

    args = parser.parse_args()
    if (args.configFile):
        config = yaml.safe_load(open(args.configFile))
        api_key = config['API-KEY']
        mongo_connection = config['mongo_connection']

    client = MongoClient(mongo_connection)
    musicblogs_database = client.musicblogs
    posts_collection= musicblogs_database['posts.'+args.blogId]


    posts_in_blog = posts_collection.find()
    posts_map = \
        { p['postId']: BlogPost(
               postId=p['postId'], title=p['title'], videoId=p['videoId'], content=p['content'], labels=p.get('labels',0), url=p.get('url', ''),
               amara_embed=p.get('amara_embed', '')
            ) for p in posts_in_blog
        }


    verify_blog_collection(posts_collection, blogId=args.blogId, apiKey=api_key, data=posts_map )
