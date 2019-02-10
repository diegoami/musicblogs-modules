
import argparse
import os
from dotenv import load_dotenv
load_dotenv()
from blogspotapi import BlogClient, BlogPost, BlogRepository

import yaml


def update_blog_collection(blog_repository, blog_client, blog_id):


    for blog_post in blog_client.iterate_blog_posts(blog_id):
        blog_repository.update_blog_post(blog_post)
    blog_repository.delete_old_posts()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')
    api_key = os.getenv("BLOG-API-KEY")
    mongo_connection = os.getenv("mongo_connection")
    args = parser.parse_args()
    if (args.configFile):
        config = yaml.safe_load(open(args.configFile))
        blog_api_key = config['API-KEY']
        mongo_connection = config['mongo_connection']

    blog_repository = BlogRepository(mongo_connection, args.blogId)
    blog_client = BlogClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    update_blog_collection(blog_repository=blog_repository, blog_client=blog_client, blog_id=args.blogId)
