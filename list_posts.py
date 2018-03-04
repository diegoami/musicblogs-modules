
import argparse
from pymongo import MongoClient

from legacy.blogspot_tools import iterate_blog_posts, iterate_title_and_videos, BlogPost
from tools.tool_blog_client import stripHtmlTags
import yaml


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.configFile))
    client = MongoClient(config['mongo_connection'])
    musicblogs_database = client.musicblogs
    posts_collection= musicblogs_database['posts.'+args.blogId]

    for blog_post in iterate_blog_posts(args.blogId, config['API-KEY']):
        for blogPost in iterate_title_and_videos(blog_post):
            print(blogPost._asdict())
            #print(blogPost.id, blogPost.title, blogPost.videoId, stripHtmlTags(blogPost.content))
            #posts_collection.insert({"postId": blogPost.postId, "title": blogPost.title, "videoId": blogPost.videoId, "content" : stripHtmlTags(blogPost.content)})
