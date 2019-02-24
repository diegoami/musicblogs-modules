from blogspotapi import BlogRepository
from amara.amara_env import amara_headers
import argparse
import os
from youtube3 import YoutubeClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--blogId', type=str)
    parser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    args = parser.parse_args()

    blog_repository = BlogRepository(args.mongo_connection, args.blogId)
    blog_repository.save_to_videos()
