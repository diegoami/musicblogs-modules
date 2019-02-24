from blogspotapi import BlogRepository
from amara.amara_env import amara_headers
import argparse
import os
from youtube3 import YoutubeClient


def verify_blog_collection(blog_repository, youtube_client, blog_id):
    for post_id, blog_post in blog_repository.posts_map.items():
        validLink = youtube_client.verify_video(blog_post.videoId)
        if not validLink:
            print('=========================================================')
            print(u'MISSING VIDEO {} IN POST {}'.format(blog_post.videoId, blog_post.postId))
            print('=========================================================')
        else:
            print(u'Successfully processed videos {} in post {} '.format(blog_post.videoId, blog_post.postId))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--blogId', type=str)
    parser.add_argument('--languages', type=str)
    parser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    args = parser.parse_args()

    blog_repository = BlogRepository(args.mongo_connection, args.blogId)
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))

    verify_blog_collection(blog_repository=blog_repository, youtube_client=youtube_client, blog_id=args.blogId)
