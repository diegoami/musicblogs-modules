
import argparse
import os

from blogspotapi import BlogClient, BlogPost, BlogRepository
from amara.amara_env import amara_headers


def update_blog_collection(blog_repository, blog_client, blog_id):
    for blog_post in blog_client.iterate_blog_posts(blog_id):
        blog_repository.update_blog_post(blog_post)
    blog_repository.delete_old_posts()

def update_subtitles_collection(blog_repository, blog_client, blog_id, languages_str, amara_headers):
    languages_list = languages_str.split(',')
    for blog_post in blog_client.iterate_blog_posts(blog_id):
        blog_repository.update_sub_titles(blog_post, languages_list, amara_headers)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId', type=str)
    parser.add_argument('--languages', type=str)
    parser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    parser.add_argument('--update_subtitles', dest='update_subtitles', action='store_true')
    parser.add_argument('--no-update_subtitles', dest='update_subtitles', action='store_false')
    parser.set_defaults(update_subtitles=True)
    args = parser.parse_args()

    blog_repository = BlogRepository(args.mongo_connection, args.blogId)
    blog_client = BlogClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    update_blog_collection(blog_repository, blog_client, args.blogId)
    if args.update_subtitles:
        update_subtitles_collection(blog_repository, blog_client, args.blogId, args.languages, amara_headers)
