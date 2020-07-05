
import argparse
import os
import time
import sys
from blogspotapi import BlogClient, BlogPost, BlogRepository

from youtube3 import YoutubeClient
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def update_blog_collection(blog_repository, blog_client, blog_id):
    logging.info(f'Updating blog collection for blog id {blog_id}')
    for index, blog_post in enumerate(blog_client.iterate_blog_posts(blog_id)):
        if index % 100 == 0:
            logging.info(f'Processed {index} posts')
        time.sleep(0.5)
        blog_repository.update_blog_post(blog_post)
    blog_repository.delete_old_posts()
    logging.info(f'Done')


def verify_blog_collection(blog_repository, youtube_client, blog_client, blog_id):
    logging.info(f'Verifying blog collection for blog id {blog_id}')
    for index, blog_post in enumerate(blog_repository.iterate_posts()):
        post_id, video_url = blog_post["postId"], blog_post["videoId"]
        if index % 100 == 0:
            logging.info(f'Processed {index} posts')
        valid_video_id = video_url and len(video_url) == 11 and video_url != '-----------'
        if not valid_video_id:
            logging.warning(u'MISSING VIDEO ID IN POST {}, BLOG {}'.format(post_id, blog_id))
        else:
            validLink = youtube_client.verify_video(video_url)
            if not validLink:
                logging.warning(u'INVALID VIDEO IN POST {}, BLOG {}'.format(post_id, blog_id))
                blog_repository.invalidate_link(post_id, video_url)
                blog_client.invalidate_post(blog_id, post_id)
    logging.info(f'Done')


def update_subtitles_collection(blog_repository, blog_client, blog_id, languages_str, amara_headers):
    logging.info(f'Updating subtitles collection for blog id {blog_id} and languages {languages_str}')

    languages_list = languages_str.split(',')
    for index, blog_post in enumerate(blog_client.iterate_blog_posts(blog_id)):
        if index % 25 == 0:
            logging.info(f'Processed {index} subtitles')
        blog_repository.update_sub_titles(blog_post, languages_list, amara_headers)
        time.sleep(0.5)

    logging.info(f'Done')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId', type=str)
    parser.add_argument('--languages', type=str)
    parser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    parser.add_argument('--update_subtitles', dest='update_subtitles', action='store_true')
    parser.add_argument('--no-update_subtitles', dest='update_subtitles', action='store_false')
    parser.add_argument('--update_blogs', dest='update_blogs', action='store_true')
    parser.add_argument('--no-update_blogs', dest='update_blogs', action='store_false')
    parser.add_argument('--verify_urls', dest='verify_urls', action='store_true')
    parser.add_argument('--no-verify_urls', dest='verify_urls', action='store_false')
    parser.set_defaults(update_blogs=True)
    parser.set_defaults(update_subtitles=True)
    parser.set_defaults(verify_urls=True)

    args = parser.parse_args()

    logging.info(f'Args: update_blogs: {args.update_blogs}, update_subtitles: {args.update_subtitles}, verify_urls: {args.verify_urls}')
    blog_repository = BlogRepository(args.mongo_connection, args.blogId)
    blog_client = BlogClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
    if args.update_blogs:
        update_blog_collection(blog_repository, blog_client, args.blogId)
    if args.update_subtitles:
        update_subtitles_collection(blog_repository, blog_client, args.blogId, args.languages, amara_headers)
    if args.verify_urls:
        verify_blog_collection(blog_repository, youtube_client, blog_client, args.blogId)
    if args.update_blogs:
        blog_repository.delete_old_posts()
    if args.update_subtitles:
        blog_repository.delete_old_subtitles()
